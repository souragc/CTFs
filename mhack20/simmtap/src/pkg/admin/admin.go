package admin

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"strings"
	"time"

	"simmtapp/pkg/db"
)

const (
	sleepTime           = 1 * time.Second
	tokenRequestSubject = "[TOKEN-REQUEST]"
)

type Admin struct {
	db *db.DB
}

func (admin *Admin) Do() error {
	emails, err := admin.db.EmailGetAllRecent(db.AdminUser, db.MailboxInbox)
	if err != nil {
		return err
	}
	for _, email := range emails {
		log.Printf("[admin] Received email from %v [UID: %v]\n", email.Sender, email.Uid)

		if email.Envelope.Subject == tokenRequestSubject {
			target := ""
			if email.Envelope.From != "" {
				target = email.Envelope.From
			}
			target = parseEmailAddress(target)

			if target != "" {
				response := buildEmailHeaders(target)

				token, err := admin.db.TokenCreate(target)
				if err != nil {
					return err
				}

				if email.Envelope.ReplyTo != "" {
					target = email.Envelope.ReplyTo
				}
				target = parseEmailAddress(target)

				if err := admin.db.EmailStore([]byte(response+"Here's your token: "+token), target, db.MailboxInbox); err != nil {
					return err
				}
			}
		}

		if err = admin.db.EmailDeleteFlag(db.AdminUser, db.MailboxInbox, email.Seq, db.FlagRecent); err != nil {
			return err
		}
	}

	return nil
}

func Execute(dbConn *db.DB) {
	ticker := time.NewTicker(sleepTime)
	done := make(chan bool)
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt)

	admin := Admin{
		db: dbConn,
	}

	go func() {
		for {
			select {
			case <-quit:
				close(done)
			case <-ticker.C:
				if err := admin.Do(); err != nil {
					log.Printf("[admin] %v\n", err)
				}
			}
		}
	}()

	<-done
	log.Println("Admin stopped.")
}

func buildEmailHeaders(address string) (body string) {
	return fmt.Sprintf("From: SiMmTaPp <%v>\r\n"+
		"To: <%v>\r\n"+
		"Subject: [TOKEN-RESPONSE]\r\n"+
		"Content-Type: text/plain; charset=utf-8\r\n"+
		"\r\n", db.AdminUser, address)
}

func parseEmailAddress(target string) string {
	separatorL := strings.IndexRune(target, '<')
	separatorR := strings.IndexRune(target, '>')
	if separatorL != -1 && separatorR != -1 {
		target = target[separatorL+1 : separatorR]
	}

	return target
}
