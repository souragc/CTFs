package db

import (
	"fmt"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

var defaultMessage = "From: %s\r\nSubject: Welcome\r\nTo: %s\r\nContent-Type: text/plain\r\nWelcome dear,\nHope you're doing well.\nThrough these trying times we need to stick together.\nRemember to wear a mask.\nCheers\n"

type userEntry struct {
	Username string `bson:"username"`
	Password string `bson:"password"`
}

func (db *DB) UserInit(username string, password string) (err error) {
	if err = db.userCreate(username, password); err != nil {
		return err
	}
	for _, mailbox := range defaultMailboxes {
		if err = db.MailboxCreate(username, mailbox); err != nil {
			return err
		}
	}
	private := fmt.Sprintf("%v-%v", MailboxPrivate, username)
	if err = db.MailboxCreate(username, private); err != nil {
		return err
	}

	if username != AdminUser {
		if err = db.EmailStoreForRecipients([]byte(fmt.Sprintf(defaultMessage, AdminUser, username)), AdminUser, []string{username}); err != nil {
			return err
		}
	}
	return nil
}

func (db *DB) userCreate(username string, password string) (err error) {
	newUser := userEntry{username, password}
	_, err = db.users.InsertOne(db.ctx, newUser)
	return err
}

func (db *DB) UserExists(user string) (userExists bool, err error) {
	var result userEntry
	err = db.users.FindOne(db.ctx, bson.M{"username": user}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	return true, nil
}

func (db *DB) UserGetPassword(user string) (password string, err error) {
	var result userEntry
	err = db.users.FindOne(db.ctx, bson.M{"username": user}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return "", fmt.Errorf("the user does not exist")
	}
	if err != nil {
		return "", err
	}
	return result.Password, nil
}
