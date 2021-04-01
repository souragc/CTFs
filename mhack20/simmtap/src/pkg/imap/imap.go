package imap

import (
	"bufio"
	"bytes"
	"encoding/base64"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"regexp"
	"sort"
	"strconv"
	"strings"

	"simmtapp/pkg/db"
)

const (
	serverHello        = "OK IMAP Service Ready"
	serverBye          = "BYE See you!"
	badNullCommand     = "BAD Null command"
	badCommand         = "BAD Command"
	badMissingCommand  = "BAD Missing command"
	badNumberArguments = "BAD Wrong number of arguments given"
	badParseCommand    = "BAD Could not parse command"
	noServerBug        = "NO Internal error"
	okSearchCommand    = "OK SEARCH completed"
	cmdNoop            = "NOOP"
	cmdLogout          = "LOGOUT"
	cmdCapability      = "CAPABILITY"
	cmdLogin           = "LOGIN"
	cmdAuthenticate    = "AUTHENTICATE"
	cmdList            = "LIST"
	cmdSelect          = "SELECT"
	cmdAppend          = "APPEND"
	cmdCreate          = "CREATE"
	cmdDelete          = "DELETE"
	cmdRename          = "RENAME"
	cmdSubscribe       = "SUBSCRIBE"
	cmdLsub            = "LSUB"
	cmdFetch           = "FETCH"
	cmdStore           = "STORE"
	cmdExpunge         = "EXPUNGE"
	cmdSearch          = "SEARCH"
	cmdClose           = "CLOSE"
	cmdUid             = "UID"
	AUTHPLAIN          = "PLAIN"
	AUTHCUSTOM         = "TOKEN"
)

type imapConn struct {
	conn    net.Conn
	scanner *bufio.Scanner
	db      *db.DB
	state   imapState
	user    string
	mailbox string
	private bool
}

type imapState int

const (
	NotAuthenticated imapState = iota
	Authenticated    imapState = iota
	Selected         imapState = iota
	Logout           imapState = iota
)

func (c *imapConn) writeTagged(tag string, msg string) (err error) {
	if tag != "" {
		msg = tag + " " + msg + "\r\n"
	} else {
		msg = msg + "\r\n"
	}
	_, err = c.conn.Write([]byte(msg))
	return err
}

func parseArguments(s string) ([]string, error) {
	var result []string
	var cursor int
	var inString, inParent bool

	if strings.Count(s, "\"")%2 == 1 ||
		strings.Count(s, "(") != strings.Count(s, ")") ||
		strings.Count(s, "[") != strings.Count(s, "]") ||
		strings.Count(s, "{") != strings.Count(s, "}") {
		return nil, errors.New("couldn't parse arguments")
	}

	for i, r := range s {
		if r == ' ' && !inString && !inParent {
			result = append(result, s[cursor:i])
			cursor = i + 1
		} else if r == '"' {
			inString = !inString
		} else if r == '(' {
			inParent = true
		} else if r == ')' {
			inParent = false
		}
	}

	return append(result, s[cursor:]), nil
}

func HandleIMAPConnection(conn net.Conn, dbConn *db.DB) {
	defer conn.Close()

	c := imapConn{
		conn:    conn,
		db:      dbConn,
		state:   NotAuthenticated,
		user:    "",
		mailbox: "",
	}

	if err := c.writeTagged("*", serverHello); err != nil {
		log.Println(err)
		return
	}

	scanner := bufio.NewScanner(conn)
	c.scanner = scanner
LOOP:
	for scanner.Scan() {
		if scanner.Err() != nil {
			log.Println(scanner.Err())
			return
		}
		line := scanner.Text()

		parts := strings.SplitN(line, " ", 3)
		tag := parts[0]
		if tag == "" {
			if err := c.writeTagged("*", badNullCommand); err != nil {
				log.Println(err)
				return
			}
			continue LOOP
		}

		if len(parts) == 1 {
			if err := c.writeTagged(tag, badMissingCommand); err != nil {
				log.Println(err)
				return
			}
			continue LOOP
		}
		command := strings.ToUpper(parts[1])

		var args []string
		if len(parts) > 2 {
			parsedArgs, err := parseArguments(parts[2])
			if err != nil {
				log.Println(err)
				if err := c.writeTagged(tag, badParseCommand); err != nil {
					log.Println(err)
					return
				}
				continue LOOP
			}
			args = parsedArgs
		}

		allowed := false
		for _, state := range allowedCmd[command] {
			if c.state == state {
				allowed = true
				break
			}
		}
		if !allowed {
			if err := c.writeTagged(tag, badCommand); err != nil {
				log.Println(err)
				return
			}
			continue LOOP
		}
		handler, ok := handlers[command]
		if !ok {
			if err := c.writeTagged(tag, badCommand); err != nil {
				log.Println(err)
				return
			}
			continue LOOP
		}

		for i, arg := range args {
			if len(arg) >= 2 && arg[0] == '"' && arg[len(arg)-1] == '"' {
				args[i] = arg[1 : len(arg)-1]
			}
		}

		if err := handler(&c, tag, args); err != nil {
			log.Printf("[handle%v] %v\n", command, err)
			return
		}

		if c.state == Logout {
			if err := c.writeTagged("*", serverBye); err != nil {
				log.Println(err)
			}
			return
		}
	}
}

type handlerFunc = func(c *imapConn, tag string, args []string) (err error)

var allowedCmd = map[string][]imapState{
	cmdNoop:         {NotAuthenticated, Authenticated, Selected},
	cmdLogout:       {NotAuthenticated, Authenticated, Selected},
	cmdCapability:   {NotAuthenticated, Authenticated, Selected},
	cmdLogin:        {NotAuthenticated},
	cmdAuthenticate: {NotAuthenticated},
	cmdList:         {Authenticated, Selected},
	cmdSelect:       {Authenticated, Selected},
	cmdAppend:       {Authenticated, Selected},
	cmdCreate:       {Authenticated, Selected},
	cmdDelete:       {Authenticated, Selected},
	cmdRename:       {Authenticated, Selected},
	cmdSubscribe:    {Authenticated, Selected},
	cmdLsub:         {Authenticated, Selected},
	cmdFetch:        {Selected},
	cmdStore:        {Selected},
	cmdExpunge:      {Selected},
	cmdSearch:       {Selected},
	cmdClose:        {Selected},
	cmdUid:          {Selected},
}

var handlers = map[string]handlerFunc{
	cmdNoop:         handleNOOP,
	cmdLogout:       handleLOGOUT,
	cmdCapability:   handleCAPABILITY,
	cmdLogin:        handleLOGIN,
	cmdAuthenticate: handleAUTHENTICATE,
	cmdList:         handleLIST,
	cmdSelect:       handleSELECT,
	cmdAppend:       handleAPPEND,
	cmdCreate:       handleCREATE,
	cmdDelete:       handleDELETE,
	cmdRename:       handleRENAME,
	cmdSubscribe:    handleSUBSCRIBE,
	cmdLsub:         handleLIST,
	cmdFetch:        handleFETCH,
	cmdStore:        handleSTORE,
	cmdExpunge:      handleEXPUNGE,
	cmdSearch:       handleSEARCH,
	cmdClose:        handleCLOSE,
	cmdUid:          handleUID,
}

func handleSUBSCRIBE(c *imapConn, tag string, args []string) (err error) {
	// Thunderbird doesn't work properly without this ¯\_(ツ)_/¯
	return c.writeTagged(tag, "OK SILLY BIRD")
}

func handleNOOP(c *imapConn, tag string, args []string) (err error) {
	// Force update (Thunderbird workaround)
	if metadata, err := c.db.MailboxGetMetadata(c.user, c.mailbox); err != nil {
		return err
	} else {
		if err := c.writeTagged("*", fmt.Sprintf("%v EXISTS", metadata.Exist)); err != nil {
			return err
		}
	}

	return c.writeTagged(tag, "OK NOOP completed")
}

func handleLOGOUT(c *imapConn, tag string, args []string) (err error) {
	c.state = Logout
	return c.writeTagged(tag, "OK LOGOUT completed")
}

func handleCAPABILITY(c *imapConn, tag string, args []string) (err error) {
	var caps string
	switch c.state {
	case NotAuthenticated:
		caps = fmt.Sprintf("IMAP4rev1 AUTH=%v AUTH=%v", AUTHPLAIN, AUTHCUSTOM)
	case Authenticated:
		caps = "IMAP4rev1 SELECT"
	case Selected:
		caps = "IMAP4rev1"
	}
	msg := fmt.Sprintf("CAPABILITY %v", caps)
	if err = c.writeTagged("*", msg); err != nil {
		return err
	}
	err = c.writeTagged(tag, "OK CAPABILITY completed")
	return err
}

func handleLOGIN(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 2 {
		err = c.writeTagged(tag, badNumberArguments)
		return err
	}
	username := args[0]
	password := args[1]
	if ok, msg, err := authPlain(c.db, username, password); err != nil {
		return err
	} else if !ok {
		return c.writeTagged(tag, msg)
	}
	c.state = Authenticated
	c.user = username
	err = c.writeTagged(tag, "OK LOGIN completed")
	return err
}

func handleAUTHENTICATE(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 1 {
		err = c.writeTagged(tag, badNumberArguments)
		return err
	}
	mode := args[0]
	var ok bool
	var msg string
	var username string
	switch mode {
	case AUTHPLAIN:
		if _, err = c.conn.Write([]byte("+\r\n")); err != nil {
			return err
		}
		_ = c.scanner.Scan()
		if c.scanner.Err() != nil {
			log.Println(c.scanner.Err())
			return
		}
		enc := c.scanner.Text()
		res, err := base64.StdEncoding.DecodeString(enc)
		if err != nil {
			return err
		}
		creds := bytes.Split(res, []byte{0})
		username = string(creds[1])
		password := string(creds[2])
		if ok, msg, err = authPlain(c.db, username, password); err != nil {
			return err
		} else if !ok {
			return c.writeTagged(tag, msg)
		}
	case AUTHCUSTOM:
		if _, err = c.conn.Write([]byte("+\r\n")); err != nil {
			return err
		}
		_ = c.scanner.Scan()
		if c.scanner.Err() != nil {
			log.Println(c.scanner.Err())
			return
		}
		enc := c.scanner.Text()
		token, err := base64.StdEncoding.DecodeString(enc)
		if err != nil {
			return err
		}
		if username, msg, err = authCustom(c.db, string(token)); err != nil {
			return err
		} else if username == "" {
			return c.writeTagged(tag, msg)
		}
		c.private = true
		ok = true
	default:
		msg = fmt.Sprintf("BAD Unknown authentication mode")
		ok = false
	}
	if !ok {
		return c.writeTagged(tag, msg)
	}
	c.state = Authenticated
	c.user = username
	err = c.writeTagged(tag, "OK AUTHENTICATE completed")
	return err
}

func authPlain(d *db.DB, username string, password string) (ok bool, msg string, err error) {
	ok, err = d.UserExists(username)
	if err != nil {
		return false, "", err
	}
	if !ok {
		return false, "NO The user does not exist", nil
	}
	p, err := d.UserGetPassword(username)
	if err != nil {
		return false, "", err
	}
	if password != p {
		return false, "NO The password is wrong", nil
	}
	return true, "", nil
}

func authCustom(d *db.DB, token string) (username string, msg string, err error) {
	username, err = d.TokenGetUser(token)
	if err != nil {
		return "", "", err
	}
	if username == "" {
		return "", "NO The token does not exist", nil
	}
	return username, "", nil
}

func handleLIST(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 2 {
		err = c.writeTagged(tag, badNumberArguments)
		return err
	}

	if args[1] == "" {
		if err = c.writeTagged("*", "LIST (\\Noselect) \"/\" \"/\""); err != nil {
			return err
		}
	} else {
		reference := args[0]
		if len(reference) > 1 && reference[0] == '"' && reference[len(reference)-1] == '"' {
			reference = reference[1 : len(reference)-1]
		}

		mailbox := args[1]
		if len(mailbox) > 1 && mailbox[0] == '"' && mailbox[len(mailbox)-1] == '"' {
			mailbox = mailbox[1 : len(mailbox)-1]
		}

		query := reference + mailbox
		query = strings.ReplaceAll(query, "\\", "\\\\")
		query = strings.ReplaceAll(query, "^", "\\^")
		query = strings.ReplaceAll(query, "$", "\\$")
		query = strings.ReplaceAll(query, ".", "\\.")
		query = strings.ReplaceAll(query, "|", "\\|")
		query = strings.ReplaceAll(query, "?", "\\?")
		query = strings.ReplaceAll(query, "+", "\\+")
		query = strings.ReplaceAll(query, "(", "\\(")
		query = strings.ReplaceAll(query, ")", "\\)")
		query = strings.ReplaceAll(query, "[", "\\[")
		query = strings.ReplaceAll(query, "{", "\\{")
		query = strings.ReplaceAll(query, "*", ".*")
		query = fmt.Sprintf("^%v$", query)

		mailboxes, err := c.db.MailboxSearch(c.user, query)
		if err != nil {
			return err
		}
		for _, mailbox := range mailboxes {
			if strings.HasPrefix(mailbox.Mailbox, db.MailboxPrivate) && !c.private {
				continue
			}
			if !strings.HasPrefix(mailbox.Mailbox, db.MailboxPrivate) && c.private {
				continue
			}

			mailboxAttributes := "\\HasNoChildren"
			if mailbox.Mailbox == db.MailboxSent {
				mailboxAttributes += " \\Sent"
			} else if mailbox.Mailbox == db.MailboxTrash {
				mailboxAttributes += " \\Trash"
			}

			msg := fmt.Sprintf("LIST (%v) \"/\" \"%v\"", mailboxAttributes, mailbox.Mailbox)
			if err = c.writeTagged("*", msg); err != nil {
				return err
			}
		}
	}

	return c.writeTagged(tag, "OK Completed")
}

func handleSELECT(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 1 {
		err = c.writeTagged(tag, badNumberArguments)
		return err
	}
	mailbox := strings.ToUpper(args[0])
	if mailbox != db.MailboxInbox {
		mailbox = args[0]
	}

	ok, err := c.db.MailboxExists(c.user, mailbox)
	if err != nil {
		return err
	}
	if !ok {
		err = c.writeTagged(tag, "NO No such mailbox")
		if err != nil {
			return err
		}
		return nil
	}

	c.mailbox = mailbox
	c.state = Selected

	metadata, err := c.db.MailboxGetMetadata(c.user, mailbox)
	if err != nil {
		return err
	}
	msg := fmt.Sprintf("%d EXISTS", metadata.Exist)
	if err = c.writeTagged("*", msg); err != nil {
		return err
	}
	msg = fmt.Sprintf("%d RECENT", metadata.Recent)
	if err = c.writeTagged("*", msg); err != nil {
		return err
	}
	msg = fmt.Sprintf("OK [UNSEEN %d] Message %d is first unseen", metadata.Unseen, metadata.Unseen)
	if err = c.writeTagged("*", msg); err != nil {
		return err
	}
	msg = fmt.Sprintf("OK [UIDNEXT %d] Predicted next UID", metadata.NextUID)
	if err = c.writeTagged("*", msg); err != nil {
		return err
	}
	msg = fmt.Sprintf("FLAGS (%v)", db.SupportedFlags)
	if err = c.writeTagged("*", msg); err != nil {
		return err
	}
	msg = fmt.Sprintf("OK [READ-WRITE] SELECT completed")
	if err = c.writeTagged(tag, msg); err != nil {
		return err
	}
	return nil
}

func handleAPPEND(c *imapConn, tag string, args []string) (err error) {
	if len(args) < 2 {
		return c.writeTagged(tag, badNumberArguments)
	}

	lastArg := args[len(args)-1]

	mailbox := strings.ToUpper(args[0])
	if mailbox != db.MailboxInbox {
		mailbox = args[0]
	}
	if ok, err := c.db.MailboxExists(c.user, mailbox); err != nil {
		return err
	} else if !ok {
		return c.writeTagged(tag, "NO [TRYCREATE] No such mailbox")
	}

	if ok, err := regexp.MatchString("^{[0-9]+}$", lastArg); err != nil {
		return err
	} else if !ok {
		return c.writeTagged(tag, badParseCommand)
	}

	numBytes, err := strconv.ParseUint(lastArg[1:len(lastArg)-1], 10, 32)
	if err != nil {
		return err
	}

	if numBytes > db.EmailMaxSize {
		return c.writeTagged(tag, fmt.Sprintf("NO Data length exceeds limit of %v", db.EmailMaxSize))
	}

	err = c.writeTagged("+", "Ready for literal data")
	if err != nil {
		return err
	}

	buffer := make([]byte, numBytes)
	if _, err := io.ReadFull(c.conn, buffer); err != nil {
		return err
	}

	if err = c.db.EmailStore(buffer, c.user, mailbox); err != nil {
		return err
	}

	buffer = make([]byte, 2)
	if _, err := io.ReadFull(c.conn, buffer); err != nil {
		return err
	}

	return c.writeTagged(tag, "OK APPEND completed")
}

func handleCREATE(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 1 {
		return c.writeTagged(tag, badNumberArguments)
	}

	mailbox := args[0]

	if strings.ToUpper(mailbox) == db.MailboxInbox {
		return c.writeTagged(tag, "NO The mailbox already exists")
	}

	if strings.HasPrefix(mailbox, db.MailboxPrivate) {
		return c.writeTagged(tag, "NO Can't create a private mailbox")
	}
	if ok, err := c.db.MailboxExists(c.user, mailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	} else if ok {
		return c.writeTagged(tag, "NO The mailbox already exists")
	}

	if err = c.db.MailboxCreate(c.user, mailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	}

	return c.writeTagged(tag, "OK CREATE completed")
}

func handleDELETE(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 1 {
		return c.writeTagged(tag, badNumberArguments)
	}

	mailbox := strings.ToUpper(args[0])
	if mailbox != db.MailboxInbox {
		mailbox = args[0]
	} else {
		return c.writeTagged(tag, "NO Cannot delete mailbox with that name")
	}
	if ok, err := c.db.MailboxExists(c.user, mailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	} else if !ok {
		return c.writeTagged(tag, "NO Mailbox doesn't exist")
	}

	if err = c.db.MailboxDelete(c.user, mailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	}

	return c.writeTagged(tag, "OK DELETE completed")
}

func handleRENAME(c *imapConn, tag string, args []string) (err error) {
	if len(args) != 2 {
		return c.writeTagged(tag, badNumberArguments)
	}

	oldMailbox := strings.ToUpper(args[0])
	if oldMailbox != db.MailboxInbox {
		oldMailbox = args[0]
	}
	if ok, err := c.db.MailboxExists(c.user, oldMailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	} else if !ok {
		return c.writeTagged(tag, "NO Mailbox doesn't exist")
	}

	newMailbox := strings.ToUpper(args[1])
	if newMailbox != db.MailboxInbox {
		newMailbox = args[1]
	}
	if ok, err := c.db.MailboxExists(c.user, newMailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	} else if ok {
		return c.writeTagged(tag, "NO A mailbox with that name already exists")
	}

	if err = c.db.MailboxRename(c.user, oldMailbox, newMailbox); err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	}

	return c.writeTagged(tag, "OK RENAME completed")
}

func handleFETCH(c *imapConn, tag string, args []string) (err error) {

	if len(args) < 2 {
		err = c.writeTagged(tag, badNumberArguments)
		return err
	}

	return handleFetchCommon(c, tag, args[0], strings.Join(args[1:], " "), false)
}

func handleFetchCommon(c *imapConn, tag string, sequenceSet string, fetchArg string, isUid bool) (err error) {

	if ok, err := regexp.MatchString("^[0-9:*,]+$", sequenceSet); err != nil {
		return err
	} else if !ok {
		return c.writeTagged(tag, badParseCommand)
	}

	start, end, err := parseSequenceSet(c, sequenceSet, isUid)
	if err != nil {
		err = c.writeTagged(tag, badParseCommand)
		return err
	}

	var result []db.EmailWithMetadata
	if isUid {
		result, err = c.db.EmailGetWithUIDRange(c.user, c.mailbox, int(start), int(end))
		if err != nil {
			return err
		}
	} else {
		result, err = c.db.EmailGetWithSeqRange(c.user, c.mailbox, int(start), int(end))
		if err != nil {
			return err
		}
	}

	for _, entry := range result {
		if fetchArg == "(FLAGS)" {
			dbFlags, err := c.db.EmailGetFlags(c.user, c.mailbox, entry.Seq)
			if err != nil {
				return err
			}

			msg := fmt.Sprintf("%v FETCH (FLAGS (%v))", entry.Seq, strings.Join(dbFlags, " "))
			if isUid {
				msg = fmt.Sprintf("%v FETCH (FLAGS (%v) UID %v)", entry.Seq, strings.Join(dbFlags, " "), entry.Uid)
			}

			if err := c.writeTagged("*", msg); err != nil {
				return err
			}
		} else if fetchArg == "(UID RFC822.SIZE FLAGS BODY.PEEK[HEADER.FIELDS (From To Cc Bcc Subject Date Message-ID Priority X-Priority References Newsgroups In-Reply-To Content-Type Reply-To)])" {

			dbFlags, err := c.db.EmailGetFlags(c.user, c.mailbox, entry.Seq)
			if err != nil {
				return err
			}

			msg := fmt.Sprintf("%v FETCH (FLAGS (%v) UID %v RFC822.SIZE %v BODY[HEADER.FIELDS (From To Cc Bcc Subject Date Message-ID Priority X-Priority References Newsgroups In-Reply-To Content-Type Reply-To)] {%v}\r\n%v)", entry.Seq, strings.Join(dbFlags, " "), entry.Uid, len(entry.Body), len(entry.Body), string(entry.Body))
			if err := c.writeTagged("*", msg); err != nil {
				return err
			}
		} else if fetchArg == "(UID RFC822.SIZE BODY.PEEK[])" {

			msg := fmt.Sprintf("%v FETCH (UID %v RFC822.SIZE %v BODY[] {%v}\r\n%v)", entry.Seq, entry.Uid, len(entry.Body), len(entry.Body), string(entry.Body))
			if err := c.writeTagged("*", msg); err != nil {
				return err
			}
		} else if fetchArg == "(RFC822)" {
			msg := fmt.Sprintf("%v FETCH (BODY[] {%v}\r\n%v)", entry.Seq, len(entry.Body), string(entry.Body))
			if isUid {
				msg = fmt.Sprintf("%v FETCH (BODY[] {%v}\r\n%v UID %v)", entry.Seq, len(entry.Body), string(entry.Body), entry.Uid)
			}

			err = c.writeTagged("*", msg)
			if err != nil {
				return err
			}
		} else {
			err = c.writeTagged(tag, badParseCommand)
			if err != nil {
				return err
			}
		}
	}

	return c.writeTagged(tag, "OK Completed")
}

func parseSequenceNumber(c *imapConn, input string, isUid bool) (value uint32, err error) {
	if input == "*" {
		var value uint32
		if isUid {
			value, err = c.db.EmailGetHighestUid(c.user, c.mailbox)
			if err != nil {
				log.Printf("EmailGetHighestUid: %v\n", err)
				return 0, err
			}
		} else {
			value, err = c.db.EmailGetHighestSeq(c.user, c.mailbox)
			if err != nil {
				log.Printf("EmailGetHighestSeq: %v\n", err)
				return 0, err
			}
		}

		return value, nil
	} else {

		value, err := strconv.ParseUint(input, 10, 32)
		if err != nil {
			return 0, err
		}
		if value == 0 {
			return 0, errors.New("parseSequenceNumber: nz-number cannot be 0")
		}
		return uint32(value), nil
	}
}

func parseSequenceSet(c *imapConn, sequenceSet string, isUid bool) (start uint32, end uint32, err error) {
	if separator := strings.IndexRune(sequenceSet, ':'); separator != -1 {

		start, err = parseSequenceNumber(c, sequenceSet[:separator], isUid)
		if err != nil {
			return 0, 0, err
		}
		end, err = parseSequenceNumber(c, sequenceSet[separator+1:], isUid)
		if err != nil {
			return 0, 0, err
		}

		if start > end {
			start, end = end, start
		}
	} else {

		val, err := parseSequenceNumber(c, sequenceSet, isUid)
		if err != nil {
			return 0, 0, err
		}
		start, end = val, val
	}
	return start, end, nil
}

func parseSequenceRange(c *imapConn, input string, isUid bool) ([]uint32, error) {
	tmp := make(map[uint32]struct{})
	for _, x := range strings.Split(input, ",") {
		start, end, err := parseSequenceSet(c, x, isUid)
		if err != nil {
			return nil, err
		}

		if start == end {
			tmp[start] = struct{}{}
		} else {

			for i := start; i <= end; i++ {
				tmp[i] = struct{}{}
			}
		}
	}

	sequence := make([]uint32, 0, len(tmp))
	for k := range tmp {
		sequence = append(sequence, k)
	}
	sort.Slice(sequence, func(i, j int) bool {
		return sequence[i] < sequence[j]
	})

	return sequence, nil
}

func handleSTORE(c *imapConn, tag string, args []string) (err error) {
	return handleStoreGeneric(c, tag, args, false)
}

func handleStoreGeneric(c *imapConn, tag string, args []string, isUid bool) (err error) {

	if len(args) < 3 {
		err = c.writeTagged(tag, badNumberArguments)
		return err
	}

	if ok, err := regexp.MatchString("^[0-9:*,]+$", args[0]); err != nil {
		return err
	} else if !ok {
		return c.writeTagged(tag, badParseCommand)
	}

	sequence, err := parseSequenceRange(c, args[0], isUid)
	if err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	}

	operation := strings.ToUpper(args[1])
	silent := false
	if strings.HasSuffix(operation, ".SILENT") {
		operation = strings.TrimSuffix(operation, ".SILENT")
		silent = true
	}

	if operation != "FLAGS" && operation != "+FLAGS" && operation != "-FLAGS" {
		return c.writeTagged(tag, badParseCommand)
	}

	re, err := regexp.Compile("\\\\[a-zA-Z]+")
	if err != nil {
		if err = c.writeTagged(tag, noServerBug); err != nil {
			return err
		}
		return err
	}
	flags := re.FindAllString(args[2], -1)

	for _, flag := range flags {
		ok := false
		for _, supported := range db.SupportedFlagsSlice {
			if flag == supported {
				ok = true
				break
			}
		}
		if !ok {
			return c.writeTagged(tag, fmt.Sprintf("BAD Invalid flag %v", flag))
		}
	}

	for _, emailId := range sequence {

		if _, err = c.db.EmailGetWithNumber(c.user, c.mailbox, int(emailId)); err != nil {
			continue
		}

		if operation == "FLAGS" {
			err = c.db.EmailSetFlags(c.user, c.mailbox, int(emailId), flags)
			if err != nil {
				if err = c.writeTagged(tag, noServerBug); err != nil {
					return err
				}
				return err
			}
		} else {
			for _, flag := range flags {
				if operation[0] == '+' {
					err = c.db.EmailAddFlag(c.user, c.mailbox, int(emailId), flag)
					if err != nil {
						if err = c.writeTagged(tag, noServerBug); err != nil {
							return err
						}
						return err
					}
				} else {
					err = c.db.EmailDeleteFlag(c.user, c.mailbox, int(emailId), flag)
					if err != nil {
						if err = c.writeTagged(tag, noServerBug); err != nil {
							return err
						}
						return err
					}
				}
			}
		}

		if !silent {
			dbFlags, err := c.db.EmailGetFlags(c.user, c.mailbox, int(emailId))
			if err != nil {
				if err = c.writeTagged(tag, noServerBug); err != nil {
					return err
				}
				return err
			}

			if err = c.writeTagged("*", fmt.Sprintf("%v FETCH (FLAGS (%v))", emailId, strings.Join(dbFlags, " "))); err != nil {
				return err
			}
		}
	}

	return c.writeTagged(tag, "OK Success")
}

func handleEXPUNGE(c *imapConn, tag string, args []string) (err error) {
	expunged, err := c.db.EmailExpunge(c.user, c.mailbox)
	if err != nil {
		return err
	}
	for _, uid := range expunged {
		msg := fmt.Sprintf("%d EXPUNGE", uid)
		err = c.writeTagged("*", msg)
		if err != nil {
			return err
		}
	}
	return c.writeTagged(tag, "OK EXPUNGE completed")
}

func handleSEARCH(c *imapConn, tag string, args []string) (err error) {
	return handleSearchGeneric(c, tag, args, false)
}

func handleSearchGeneric(c *imapConn, tag string, args []string, isUid bool) (err error) {

	if len(args) < 1 {
		return c.writeTagged(tag, badNumberArguments)
	}

	emails, err := c.db.EmailGetAll(c.user, c.mailbox)
	if err != nil {
		return err
	}
	if len(emails) > 0 {
		line := "SEARCH"
		for _, email := range emails {
			if isUid {
				line = fmt.Sprintf("%s %d", line, email.Uid)
			} else {
				line = fmt.Sprintf("%s %d", line, email.Seq)
			}
		}
		if err = c.writeTagged("*", line); err != nil {
			return err
		}
	}

	return c.writeTagged(tag, okSearchCommand)
}

func handleCLOSE(c *imapConn, tag string, args []string) (err error) {

	if _, err = c.db.EmailExpunge(c.user, c.mailbox); err != nil {
		return err
	}
	c.state = Authenticated
	c.mailbox = ""
	return c.writeTagged(tag, "OK CLOSE completed")
}

func handleUID(c *imapConn, tag string, args []string) (err error) {
	command := strings.ToUpper(args[0])

	if command == cmdFetch {
		return handleFetchCommon(c, tag, args[1], strings.Join(args[2:], " "), true)
	} else if command == cmdSearch {
		return handleSearchGeneric(c, tag, args[1:], true)
	} else if command == cmdStore {
		return handleStoreGeneric(c, tag, args[1:], true)
	}

	return c.writeTagged(tag, badCommand)
}
