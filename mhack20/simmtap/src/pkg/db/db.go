package db

import (
	"context"
	"github.com/pkg/errors"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"simmtapp/pkg/utils"
)

const (
	dbName           = "simmtapp"
	collUsers        = "users"
	collMailboxes    = "mailboxes"
	collEmails       = "emails"
	collMailingLists = "lists"
	collTokens       = "tokens"
	emailDir         = "/emails"
	domain           = "ctf.mhackeroni.it"
	AdminUser        = "admin@" + domain
)

type DB struct {
	client    *mongo.Client
	ctx       context.Context
	users     *mongo.Collection
	mailboxes *mongo.Collection
	emails    *mongo.Collection
	lists     *mongo.Collection
	tokens    *mongo.Collection
}

func (db *DB) Connect(URI string) (err error) {
	client, err := mongo.NewClient(options.Client().ApplyURI(URI))
	if err != nil {
		return err
	}
	ctx := context.Background()
	err = client.Connect(ctx)
	if err != nil {
		return err
	}
	db.client = client
	db.ctx = ctx
	db.users = client.Database(dbName).Collection(collUsers)
	db.mailboxes = client.Database(dbName).Collection(collMailboxes)
	db.emails = client.Database(dbName).Collection(collEmails)
	db.lists = client.Database(dbName).Collection(collMailingLists)
	db.tokens = client.Database(dbName).Collection(collTokens)

	err = createUniqueIndexes(ctx, db.users, []string{"username"})
	if err != nil {
		return err
	}
	err = createIndexes(ctx, db.mailboxes, []string{"user",
		"mailbox",
	})
	if err != nil {
		return err
	}
	err = createIndexes(ctx, db.emails, []string{"recipient",
		"uid",
		"sender",
	})
	if err != nil {
		return err
	}
	err = createUniqueIndexes(ctx, db.lists, []string{"name"})
	if err != nil {
		return err
	}
	err = createUniqueIndexes(ctx, db.tokens, []string{"token"})
	if err != nil {
		return err
	}
	err = createIndexes(ctx, db.tokens, []string{"user"})
	if err != nil {
		return err
	}

	return nil
}

func (db *DB) Init() error {

	if ok, err := db.UserExists(AdminUser); err != nil {
		return err
	} else if !ok {
		if err := db.UserInit(AdminUser, utils.RandStringRunes(16)); err != nil {
			return err
		}
	}

	return nil
}

func createUniqueIndexes(ctx context.Context, c *mongo.Collection, keys []string) error {
	var models []mongo.IndexModel

	for _, k := range keys {
		models = append(models, mongo.IndexModel{
			Keys:    bson.M{k: 1},
			Options: options.Index().SetUnique(true),
		})
	}

	_, err := c.Indexes().CreateMany(ctx, models, options.CreateIndexes())
	if err != nil {
		return errors.Wrapf(err, "cannot create index for %s", c.Name)
	}
	return nil
}

func createIndexes(ctx context.Context, c *mongo.Collection, keys []string) error {
	var models []mongo.IndexModel

	for _, k := range keys {
		models = append(models, mongo.IndexModel{
			Keys: bson.M{k: 1},
		})
	}

	_, err := c.Indexes().CreateMany(ctx, models, options.CreateIndexes())
	if err != nil {
		return errors.Wrapf(err, "cannot create index for %s", c.Name)
	}
	return nil
}
