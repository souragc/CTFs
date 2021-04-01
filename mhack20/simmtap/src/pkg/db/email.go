package db

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
	"simmtapp/pkg/utils"
	"simmtapp/pkg/utils/fasthash"
)

const (
	FlagSeen       = "\\Seen"
	FlagDeleted    = "\\Deleted"
	FlagAnswered   = "\\Answered"
	FlagDraft      = "\\Draft"
	FlagRecent     = "\\Recent"
	SupportedFlags = "\\Seen \\Deleted \\Answered \\Draft \\Recent"
	EmailMaxSize   = 1024
)

var SupportedFlagsSlice = []string{FlagSeen, FlagDeleted, FlagAnswered, FlagDraft, FlagRecent}

type EmailWithMetadata struct {
	Recipient string
	Sender    string
	Uid       int
	Seq       int
	Flags     []string
	Body      []byte
	Timestamp time.Time
	Envelope  utils.EnvelopeFields
}

func (d EmailWithMetadata) String() string {
	return ""
}

type emailEntry struct {
	Recipient string               `bson:"recipient"`
	Mailbox   string               `bson:"mailbox"`
	UID       int                  `bson:"uid"`
	Seq       int                  `bson:"seq"`
	Sender    string               `bson:"sender"`
	BodyID    string               `bson:"bodyID"`
	Flags     []string             `bson:"flags"`
	Timestamp int64                `bson:"timestamp"`
	Envelope  utils.EnvelopeFields `bson:"envelope"`
}

func (db *DB) EmailStore(body []byte, user string, mailbox string) (err error) {
	if ok, err := db.UserExists(user); err != nil {
		return err
	} else if !ok {
		return fmt.Errorf("the user %v does not exist", user)
	}

	emailID, err := emailStoreBody(body)
	if err != nil {
		return err
	}

	headers := fmt.Sprintf("%s", body)
	envelope := utils.ParseEnvelopeStruct(headers)

	return db.emailPlaceInMailbox(user, mailbox, user, emailID, envelope)
}

func (db *DB) EmailStoreForRecipients(body []byte, sender string, recipients []string) (err error) {
	ok, err := db.UserExists(sender)
	if err != nil {
		return err
	}
	if !ok {
		return fmt.Errorf("the user %v does not exist", sender)
	}

	for _, recipient := range recipients {
		ok, err := db.UserExists(recipient)
		if err != nil {
			return err
		}
		if !ok {
			return fmt.Errorf("the user %v does not exist", recipient)
		}
	}

	emailID, err := emailStoreBody(body)
	if err != nil {
		return err
	}

	headers := fmt.Sprintf("%s", body)
	envelope := utils.ParseEnvelopeStruct(headers)

	for _, recipient := range recipients {
		err := db.emailPlaceInMailbox(recipient, MailboxInbox, sender, emailID, envelope)
		if err != nil {
			return err
		}
	}
	return nil
}

func emailStoreBody(body []byte) (emailID string, err error) {
	if len(body) > EmailMaxSize {
		return "", fmt.Errorf("the email body is too big: expected max %d bytes, actual %d bytes", EmailMaxSize, len(body))
	}

	stored := make([]byte, EmailMaxSize)
	copy(stored, body)
	for i := len(body); i < EmailMaxSize; i++ {
		stored[i] = 0
	}
	hash := fasthash.New()
	hash.Update(stored)
	filename := hash.Hexdigest()
	emailPath := path.Join(emailDir, filename)
	if _, err := os.Stat(emailPath); os.IsNotExist(err) {
		err = ioutil.WriteFile(emailPath, stored, 0600)
		if err != nil {
			return "", err
		}
	}
	return filename, nil
}

func (db *DB) emailPlaceInMailbox(recipient string, mailbox string, sender string, emailID string, envelope utils.EnvelopeFields) (err error) {
	metadata, err := db.MailboxGetMetadata(recipient, mailbox)
	if err != nil {
		return err
	}
	newEntry := emailEntry{
		Recipient: recipient,
		Mailbox:   mailbox,
		UID:       metadata.NextUID,
		Seq:       1 + metadata.Exist,
		Sender:    sender,
		BodyID:    emailID,
		Flags:     []string{FlagRecent},
		Timestamp: time.Now().Unix(),
		Envelope:  envelope,
	}
	_, err = db.emails.InsertOne(db.ctx, newEntry)
	if err != nil {
		return err
	}
	nextUnseen := metadata.Unseen
	if nextUnseen == 0 {
		nextUnseen = newEntry.Seq
	}
	newMetadata := MailboxMetadata{
		Exist:   metadata.Exist + 1,
		Recent:  metadata.Recent + 1,
		Unseen:  nextUnseen,
		NextUID: metadata.NextUID + 1,
	}
	err = db.MailboxSetMetadata(recipient, mailbox, newMetadata)
	return err
}

func (db *DB) EmailGetAll(user string, mailbox string) (emails []EmailWithMetadata, err error) {
	ok, err := db.UserExists(user)
	if err != nil {
		return nil, err
	}
	if !ok {
		return nil, fmt.Errorf("the user %v does not exist", user)
	}

	var results []emailEntry
	cursor, err := db.emails.Find(db.ctx, bson.M{"recipient": user, "mailbox": mailbox})
	if err != nil {
		return nil, err
	}
	if err = cursor.All(db.ctx, &results); err != nil {
		return nil, err
	}
	for _, entry := range results {
		body, err := db.emailGetBodyWithID(entry.BodyID)
		if err != nil {
			return nil, err
		}
		emails = append(emails, EmailWithMetadata{
			Recipient: entry.Recipient,
			Sender:    entry.Sender,
			Uid:       entry.UID,
			Seq:       entry.Seq,
			Flags:     entry.Flags,
			Body:      body,
			Timestamp: time.Now(),
			Envelope:  entry.Envelope,
		})
	}
	return emails, nil
}

func (db *DB) emailGetBodyWithID(emailID string) (body []byte, err error) {
	body, err = ioutil.ReadFile(path.Join(emailDir, emailID))
	if err != nil {
		return nil, err
	}

	end := len(body) - 1
	for ; body[end] == 0; end-- {
	}
	body = body[:end+1]
	return body, nil
}

func (db *DB) EmailGetWithUID(user string, mailbox string, uid int) (email EmailWithMetadata, err error) {
	ok, err := db.UserExists(user)
	if err != nil {
		return EmailWithMetadata{}, err
	}
	if !ok {
		return EmailWithMetadata{}, fmt.Errorf("the user %v does not exist", user)
	}

	var entry emailEntry
	err = db.emails.FindOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "uid": uid}).Decode(&entry)
	if err != nil {
		return EmailWithMetadata{}, err
	}
	body, err := db.emailGetBodyWithID(entry.BodyID)
	if err != nil {
		return EmailWithMetadata{}, err
	}
	email = EmailWithMetadata{
		Recipient: entry.Recipient,
		Sender:    entry.Sender,
		Uid:       entry.UID,
		Seq:       entry.Seq,
		Flags:     entry.Flags,
		Body:      body,
		Timestamp: time.Unix(entry.Timestamp, 0),
		Envelope:  entry.Envelope,
	}
	return email, nil
}

func (db *DB) EmailGetWithNumber(user string, mailbox string, sequenceNumber int) (email EmailWithMetadata, err error) {
	ok, err := db.UserExists(user)
	if err != nil {
		return EmailWithMetadata{}, err
	}
	if !ok {
		return EmailWithMetadata{}, fmt.Errorf("the user %v does not exist", user)
	}

	var entry emailEntry
	err = db.emails.FindOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "seq": sequenceNumber}).Decode(&entry)
	if err != nil {
		return EmailWithMetadata{}, err
	}
	body, err := db.emailGetBodyWithID(entry.BodyID)
	if err != nil {
		return EmailWithMetadata{}, err
	}
	email = EmailWithMetadata{
		Recipient: entry.Recipient,
		Sender:    entry.Sender,
		Uid:       entry.UID,
		Seq:       entry.Seq,
		Flags:     entry.Flags,
		Body:      body,
		Timestamp: time.Unix(entry.Timestamp, 0),
		Envelope:  entry.Envelope,
	}
	return email, nil
}

func (db *DB) EmailGetFlags(user string, mailbox string, uid int) (flags []string, err error) {
	ok, err := db.UserExists(user)
	if err != nil {
		return nil, err
	}
	if !ok {
		return nil, fmt.Errorf("the user %v does not exist", user)
	}

	var entry emailEntry
	err = db.emails.FindOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "seq": uid}).Decode(&entry)
	if err != nil {
		return nil, err
	}
	return entry.Flags, nil
}

func (db *DB) EmailSetFlags(user string, mailbox string, uid int, flags []string) (err error) {
	_, err = db.emails.UpdateOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "seq": uid}, bson.M{"$set": bson.M{"flags": flags}})
	if err != nil {
		return err
	}

	return err
}

func (db *DB) EmailAddFlag(user string, mailbox string, uid int, flag string) (err error) {
	flags, err := db.EmailGetFlags(user, mailbox, uid)
	if err != nil {
		return err
	}
	for _, f := range flags {
		if f == flag {
			return nil
		}
	}

	flags = append(flags, flag)
	_, err = db.emails.UpdateOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "seq": uid}, bson.M{"$set": bson.M{"flags": flags}})
	if err != nil {
		return err
	}

	return err
}

func (db *DB) EmailDeleteFlag(user string, mailbox string, uid int, flag string) (err error) {
	flags, err := db.EmailGetFlags(user, mailbox, uid)
	var newflags []string
	for _, f := range flags {
		if f != flag {
			newflags = append(newflags, f)
		}
	}
	_, err = db.emails.UpdateOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "seq": uid}, bson.M{"$set": bson.M{"flags": newflags}})
	if err != nil {
		return err
	}

	return err
}

func (db *DB) EmailExpunge(user string, mailbox string) (expunged []int, err error) {
	var results []emailEntry
	cursor, err := db.emails.Find(db.ctx, bson.M{"recipient": user, "mailbox": mailbox})
	if err != nil {
		return []int{}, err
	}
	if err = cursor.All(db.ctx, &results); err != nil {
		return []int{}, err
	}
	n := 0
	for _, entry := range results {
		for _, f := range entry.Flags {
			if f == FlagDeleted {
				_, err = db.emails.DeleteOne(db.ctx, entry)
				if err != nil {
					return expunged, err
				}
				expunged = append(expunged, entry.Seq-n)
				n++
			} else if n > 0 {
				_, err = db.emails.UpdateOne(
					db.ctx,
					bson.M{"recipient": entry.Recipient, "mailbox": entry.Mailbox, "uid": entry.UID},
					bson.M{"$set": bson.M{"seq": entry.Seq - n}},
				)
				if err != nil {
					return expunged, err
				}
			}
		}
	}

	metadata, err := db.MailboxGetMetadata(user, mailbox)
	if err != nil {
		return expunged, err
	}
	newMetadata := MailboxMetadata{
		Exist:   metadata.Exist - n,
		Recent:  metadata.Recent,
		Unseen:  metadata.Unseen,
		NextUID: metadata.NextUID,
	}
	err = db.MailboxSetMetadata(user, mailbox, newMetadata)
	if err != nil {
		return expunged, err
	}
	return expunged, nil
}

func (db *DB) EmailGetWithSeqRange(user string, mailbox string, start int, end int) ([]EmailWithMetadata, error) {
	cursor, err := db.emails.Find(db.ctx, bson.M{"seq": bson.M{"$gte": start, "$lte": end}, "mailbox": mailbox})
	if err != nil {
		return nil, err
	}

	res := make([]EmailWithMetadata, 0)
	for cursor.Next(db.ctx) {
		var entry emailEntry
		if err = cursor.Decode(&entry); err != nil {
			return nil, err
		}

		if strings.ToUpper(user) == strings.ToUpper(entry.Recipient) {
			body, err := db.emailGetBodyWithID(entry.BodyID)
			if err != nil {
				return nil, err
			}
			res = append(res, EmailWithMetadata{
				Recipient: entry.Recipient,
				Sender:    entry.Sender,
				Uid:       entry.UID,
				Seq:       entry.Seq,
				Flags:     entry.Flags,
				Body:      body,
				Timestamp: time.Now(),
				Envelope:  entry.Envelope,
			})
		}
	}
	return res, nil
}

func (db *DB) EmailGetWithUIDRange(user string, mailbox string, start int, end int) ([]EmailWithMetadata, error) {
	cursor, err := db.emails.Find(db.ctx, bson.M{"uid": bson.M{"$gte": start, "$lte": end}, "mailbox": mailbox})
	if err != nil {
		return nil, err
	}

	res := make([]EmailWithMetadata, 0)
	for cursor.Next(db.ctx) {
		var entry emailEntry
		if err = cursor.Decode(&entry); err != nil {
			return nil, err
		}

		if strings.ToUpper(user) == strings.ToUpper(entry.Recipient) {
			body, err := db.emailGetBodyWithID(entry.BodyID)
			if err != nil {
				return nil, err
			}
			res = append(res, EmailWithMetadata{
				Recipient: entry.Recipient,
				Sender:    entry.Sender,
				Uid:       entry.UID,
				Seq:       entry.Seq,
				Flags:     entry.Flags,
				Body:      body,
				Timestamp: time.Now(),
				Envelope:  entry.Envelope,
			})
		}
	}
	return res, nil
}

func (db *DB) EmailGetHighestSeq(user string, mailbox string) (value uint32, err error) {
	var entry emailEntry
	findOptions := options.FindOne()
	findOptions.SetSort(bson.M{"seq": -1})
	err = db.emails.FindOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox}, findOptions).Decode(&entry)
	if err != nil {
		return 0, err
	}

	return uint32(entry.Seq), nil
}

func (db *DB) EmailGetHighestUid(user string, mailbox string) (value uint32, err error) {
	var entry emailEntry
	findOptions := options.FindOne()
	findOptions.SetSort(bson.M{"uid": -1})
	err = db.emails.FindOne(db.ctx, bson.M{"recipient": user, "mailbox": mailbox}, findOptions).Decode(&entry)
	if err != nil {
		return 0, err
	}

	return uint32(entry.UID), nil
}

func (db *DB) EmailGetAllRecent(user string, mailbox string) (emails []EmailWithMetadata, err error) {
	ok, err := db.UserExists(user)
	if err != nil {
		return nil, err
	}
	if !ok {
		return nil, fmt.Errorf("the user %v does not exist", user)
	}

	var results []emailEntry
	cursor, err := db.emails.Find(db.ctx, bson.M{"recipient": user, "mailbox": mailbox, "flags": "\\Recent"})
	if err != nil {
		return nil, err
	}
	if err = cursor.All(db.ctx, &results); err != nil {
		return nil, err
	}
	for _, entry := range results {
		body, err := db.emailGetBodyWithID(entry.BodyID)
		if err != nil {
			return nil, err
		}
		emails = append(emails, EmailWithMetadata{
			Recipient: entry.Recipient,
			Sender:    entry.Sender,
			Uid:       entry.UID,
			Seq:       entry.Seq,
			Flags:     entry.Flags,
			Body:      body,
			Timestamp: time.Now(),
			Envelope:  entry.Envelope,
		})
	}
	return emails, nil
}
