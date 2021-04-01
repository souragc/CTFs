package smtp

import (
	"bufio"
	"encoding/base64"
	"fmt"
	"log"
	"net"
	"strings"

	"simmtapp/pkg/db"
)

type connectionState struct {
	recvHello      bool
	authStarted    bool
	authCompleted  bool
	username       string
	password       string
	from           []string
	to             []string
	data           []byte
	waitingForData bool
}

var (
	serverHello                = []byte("220 mhackeroni.ctf.it SMTP simmtapp\r\n")
	serverAuth                 = []byte("250-mhackeroni.ctf.it\r\n250 AUTH LOGIN\r\n")
	serverData                 = []byte("354 Send message content; end with <CRLF>.<CRLF>\r\n")
	serverBye                  = []byte("221 Bye\r\n")
	serverOK                   = []byte("250 OK\r\n")
	server334                  = []byte("334\r\n")
	serverCommandNotRecognized = []byte("500 NOT OK\r\n")
	serverBadArguments         = []byte("501 NOT OK\r\n")
	serverMessageTooBig        = []byte("554 5.3.4 Message too big for system\r\n")
	serverUsernameQ            = []byte("334 VXNlcm5hbWU6\r\n")
	serverPasswordQ            = []byte("334 UGFzc3dvcmQ6\r\n")
	serverAuthSuccessful       = []byte("235 Authentication successful\r\n")
	serverAuthFailed           = []byte("535 Authentication failed\r\n")
)

const (
	maxEmails = 5
	ehlo      = "EHLO"
	helo      = "HELO"
	mail      = "MAIL"
	rcpt      = "RCPT"
	quit      = "QUIT"
	data      = "DATA"
	rset      = "RSET"
	vrfy      = "VRFY"
	expn      = "EXPN"
	help      = "HELP"
	noop      = "NOOP"
	auth      = "AUTH"
)

func HandleSMTPConnection(conn net.Conn, dbConn *db.DB) {
	defer conn.Close()

	_, err := conn.Write(serverHello)
	if err != nil {
		log.Println(err)
		return
	}

	var connState connectionState
	scanner := bufio.NewScanner(conn)

LOOP:
	for scanner.Scan() {
		if scanner.Err() != nil {
			log.Println(scanner.Err())
			return
		}

		line := scanner.Text()

		if connState.waitingForData {
			if line == "." {
				connState.waitingForData = false
				if len(connState.data) > 0 && len(connState.data) <= db.EmailMaxSize &&
					len(connState.from) > 0 && len(connState.to) > 0 &&
					len(connState.from) < maxEmails && len(connState.to) < maxEmails {
					log.Println(connState.from)
					log.Println(connState.to)
					err = dbConn.EmailStoreForRecipients(connState.data, connState.from[0], connState.to)
					if err != nil {
						log.Println(err)
					}
					_, err = conn.Write(serverOK)
					if err != nil {
						log.Println(err)
						return
					}
				} else {
					_, err = conn.Write(serverMessageTooBig)
					if err != nil {
						log.Println(err)
						return
					}
				}
			} else {
				connState.data = append(connState.data, []byte(line)...)
				connState.data = append(connState.data, '\r', '\n')
			}
			continue
		}

		parts := strings.Split(line, " ")
		command := parts[0]

		args := parts[1:]

		if !connState.recvHello {
			if strings.ToUpper(command) == ehlo || strings.ToUpper(command) == helo {
				_, err = conn.Write(serverAuth)
				if err != nil {
					log.Println(err)
					return
				}
				connState.recvHello = true
				continue
			}
			break LOOP
		}

		if !connState.authStarted {
			if strings.ToUpper(command) == auth && len(args) >= 1 && args[0] == "LOGIN" {
				_, err = conn.Write(serverUsernameQ)
				if err != nil {
					log.Println(err)
					return
				}
				if len(args) >= 2 {
					d, err := base64.StdEncoding.DecodeString(args[1])
					if err != nil {
						log.Println(err)
						break LOOP
					}
					connState.username = fmt.Sprintf("%s", d)
				}
				connState.authStarted = true
				continue
			}
			break LOOP
		}

		if !connState.authCompleted {
			if connState.username == "" {
				d, err := base64.StdEncoding.DecodeString(command)
				if err != nil {
					log.Println(err)
					break LOOP
				}
				connState.username = fmt.Sprintf("%s", d)
				_, err = conn.Write(serverPasswordQ)
				if err != nil {
					log.Println(err)
					return
				}
				continue
			} else {
				if connState.password == "" {
					d, err := base64.StdEncoding.DecodeString(command)
					if err != nil {
						log.Println(err)
						break LOOP
					}
					connState.password = fmt.Sprintf("%s", d)
					connState.authCompleted = true

					ok, err := dbConn.UserExists(connState.username)
					if err != nil {
						log.Println(err)
						break LOOP
					}
					if ok {
						pwd, err := dbConn.UserGetPassword(connState.username)
						if err != nil {
							log.Println(err)
							break LOOP
						}
						if pwd != connState.password {
							_, err = conn.Write(serverAuthFailed)
							if err != nil {
								log.Println(err)
								return
							}
							break LOOP
						}
					} else {
						err := dbConn.UserInit(connState.username, connState.password)
						if err != nil {
							log.Println(err)
							break LOOP
						}
					}

					_, err = conn.Write(serverAuthSuccessful)
					if err != nil {
						log.Println(err)
						return
					}
					continue
				}
			}
		}

		switch strings.ToUpper(command) {
		case mail:
			if len(args) < 1 {
				if _, err := conn.Write(serverBadArguments); err != nil {
					log.Println(err)
					break LOOP
				}
				continue LOOP
			}

			e, err := extractEmail(args[0])
			if err != nil {
				log.Println(err)
				break LOOP
			}

			ok, err := dbConn.UserExists(e)
			if err != nil {
				log.Println(err)
				break LOOP
			}
			if ok {
				connState.from = append(connState.from, e)
			} else {
				break LOOP
			}

		case rcpt:
			if len(args) < 1 {
				if _, err := conn.Write(serverBadArguments); err != nil {
					log.Println(err)
					break LOOP
				}
				continue LOOP
			}

			e, err := extractEmail(args[0])
			if err != nil {
				log.Println(err)
				break LOOP
			}

			connState.to = append(connState.to, e)
		case data:
			_, err = conn.Write(serverData)
			if err != nil {
				log.Println(err)
				break LOOP
			}
			connState.waitingForData = true
			continue
		case rset:
			connState = connectionState{
				recvHello:   true,
				authStarted: true,
				username:    connState.username,
				password:    connState.password,
			}
		case expn, help, noop, vrfy:
			break
		case quit:
			break LOOP
		default:
			_, err = conn.Write(serverCommandNotRecognized)
			if err != nil {
				log.Println(err)
			}

			continue LOOP
		}

		_, err = conn.Write(serverOK)
		if err != nil {
			log.Println(err)
			return
		}
	}

	_, err = conn.Write(serverBye)
	if err != nil {
		log.Println(err)
	}
}

func extractEmail(emailField string) (string, error) {
	p := strings.Split(emailField, "<")
	if len(p) != 2 {
		return "", fmt.Errorf("invalid email")
	}
	return strings.TrimSuffix(p[1], ">"), nil
}
