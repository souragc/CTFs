package db

import (
	"fmt"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

const (
	MailboxInbox   = "INBOX"
	MailboxSent    = "Sent"
	MailboxTrash   = "Trash"
	MailboxPrivate = "Private"
)

var defaultMailboxes = []string{MailboxInbox, MailboxSent, MailboxTrash}

type MailboxEntry struct {
	User    string `bson:"user"`
	Mailbox string `bson:"mailbox"`
	Exist   int    `bson:"exist"`
	Recent  int    `bson:"recent"`
	Unseen  int    `bson:"unseen"`
	NextUID int    `bson:"nextuid"`
}

type MailboxMetadata struct {
	Exist   int
	Recent  int
	Unseen  int
	NextUID int
}

func (db *DB) MailboxCreate(user string, mailbox string) (err error) {
	newMailbox := MailboxEntry{user, mailbox, 0, 0, 0, 1}
	_, err = db.mailboxes.InsertOne(db.ctx, newMailbox)
	return err
}

func (db *DB) MailboxDelete(user string, mailbox string) (err error) {
	if _, err = db.mailboxes.DeleteOne(db.ctx, bson.M{"user": user, "mailbox": mailbox}); err != nil {
		return err
	}
	_, err = db.emails.DeleteMany(db.ctx, bson.M{"recipient": user, "mailbox": mailbox})
	return err
}

func (db *DB) MailboxRename(user string, oldMailbox string, newMailbox string) (err error) {
	if oldMailbox == MailboxInbox {
		metadata, err := db.MailboxGetMetadata(user, oldMailbox)
		if err != nil {
			return err
		}
		newMailboxEntry := MailboxEntry{user, newMailbox, metadata.Exist, metadata.Recent, metadata.Unseen, metadata.NextUID}
		if _, err = db.mailboxes.InsertOne(db.ctx, newMailboxEntry); err != nil {
			return err
		}
		if err := db.MailboxSetMetadata(user, MailboxInbox, MailboxMetadata{0, 0, 0, 1}); err != nil {
			return err
		}
	} else {
		if _, err = db.mailboxes.UpdateOne(db.ctx, bson.M{"mailbox": oldMailbox, "user": user}, bson.M{"$set": bson.M{"mailbox": newMailbox}}); err != nil {
			return err
		}
	}

	_, err = db.emails.UpdateMany(db.ctx, bson.M{"recipient": user, "mailbox": oldMailbox}, bson.M{"$set": bson.M{"mailbox": newMailbox}})
	return err
}

func (db *DB) MailboxExists(user string, mailbox string) (ok bool, err error) {
	var result MailboxEntry
	err = db.mailboxes.FindOne(db.ctx, bson.M{"mailbox": mailbox, "user": user}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	return true, nil
}

func (db *DB) MailboxSearch(user string, regex string) (mailboxes []MailboxEntry, err error) {
	cursor, err := db.mailboxes.Find(db.ctx, bson.M{"mailbox": primitive.Regex{Pattern: regex, Options: ""}, "user": user})
	if err != nil {
		return nil, err
	}

	for cursor.Next(db.ctx) {
		var result MailboxEntry
		if err = cursor.Decode(&result); err != nil {
			return nil, err
		}
		mailboxes = append(mailboxes, result)
	}

	err = cursor.Close(db.ctx)
	return mailboxes, err
}

func (db *DB) MailboxGetMetadata(user string, mailbox string) (metadata MailboxMetadata, err error) {
	var result MailboxEntry
	err = db.mailboxes.FindOne(db.ctx, bson.M{"mailbox": mailbox, "user": user}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return MailboxMetadata{}, nil
	}
	if err != nil {
		return MailboxMetadata{}, err
	}
	return MailboxMetadata{
		Exist:   result.Exist,
		Recent:  result.Recent,
		Unseen:  result.Unseen,
		NextUID: result.NextUID,
	}, nil
}

func (db *DB) MailboxSetMetadata(user string, mailbox string, metadata MailboxMetadata) (err error) {
	var result MailboxEntry
	err = db.mailboxes.FindOne(db.ctx, bson.M{"mailbox": mailbox, "user": user}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return fmt.Errorf("MailboxSetMetadata: the user does not exist")
	}
	if err != nil {
		return err
	}
	newEntry := MailboxEntry{
		user,
		mailbox,
		metadata.Exist,
		metadata.Recent,
		metadata.Unseen,
		metadata.NextUID,
	}
	_, err = db.mailboxes.UpdateOne(db.ctx, bson.M{"mailbox": mailbox, "user": user}, bson.M{"$set": newEntry})
	if err != nil {
		return err
	}
	return nil
}
