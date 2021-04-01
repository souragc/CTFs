package db

import (
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"simmtapp/pkg/utils"
)

type tokenEntry struct {
	User  string `bson:"user"`
	Token string `bson:"token"`
}

func (db *DB) TokenCreate(user string) (token string, err error) {
	token = utils.RandStringRunes(10)
	newEntry := tokenEntry{user, token}
	_, err = db.tokens.InsertOne(db.ctx, newEntry)
	return token, err
}

func (db *DB) TokenExists(token string) (ok bool, err error) {
	var result tokenEntry
	err = db.tokens.FindOne(db.ctx, bson.M{"token": token}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	return true, nil
}

func (db *DB) TokenGetUser(token string) (user string, err error) {
	var result tokenEntry
	err = db.tokens.FindOne(db.ctx, bson.M{"token": token}).Decode(&result)
	if err == mongo.ErrNoDocuments {
		return "", nil
	}
	if err != nil {
		return "", err
	}
	return result.User, nil
}
