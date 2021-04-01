package utils

import (
	"math/rand"
	"strings"
	"time"
)

type EnvelopeFields struct {
	To      []string `bson:"to"`
	From    string   `bson:"from"`
	Sender  string   `bson:"sender"`
	ReplyTo string   `bson:"replyto"`
	Cc      []string `bson:"cc"`
	Bcc     []string `bson:"bcc"`
	Subject string   `bson:"subject"`
}

var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func initRand() {
	rand.Seed(int64(time.Now().Second()))
}

func RandStringRunes(n int) string {
	initRand()
	b := make([]rune, n)
	for i := range b {
		b[i] = letterRunes[rand.Intn(len(letterRunes))]
	}
	return string(b)
}

const (
	HEADERTO                      = "To"
	HEADERFROM                    = "From"
	HEADERCC                      = "Cc"
	HEADERBCC                     = "Bcc"
	HEADERREPLYTO                 = "Reply-To"
	HEADERSENDER                  = "Sender"
	HEADERSUBJECT                 = "Subject"
	HEADERMESSAGEID               = "Message-ID"
	HEADERDATE                    = "Date"
	HEADERUSERAGENT               = "User-Agent"
	HEADERMIMEVERSION             = "MIME-Version"
	HEADERCONTENTTYPE             = "Content-Type"
	HEADERCONTENTTRANSFERENCODING = "Content-Transfer-Encoding"
	HEADERCONTENTLANGUAGE         = "Content-Language"
	HEADERINREPLYTO               = "In-Reply-To"
)

var KnownHeaders = []string{
	HEADERTO,
	HEADERFROM,
	HEADERCC,
	HEADERBCC,
	HEADERREPLYTO,
	HEADERSENDER,
	HEADERSUBJECT,
	HEADERMESSAGEID,
	HEADERDATE,
	HEADERUSERAGENT,
	HEADERMIMEVERSION,
	HEADERCONTENTTYPE,
	HEADERCONTENTTRANSFERENCODING,
	HEADERCONTENTLANGUAGE,
	HEADERINREPLYTO,
}

func ParseEnvelope(headers string) map[string]string {
	res := make(map[string]string, 0)
	for _, line := range strings.Split(headers, "\n") {
		line = strings.ReplaceAll(line, "\r", "")
		for _, h := range KnownHeaders {
			prefix := h + ": "
			if strings.HasPrefix(line, prefix) {
				res[h] = line[len(prefix):]
				break
			}
		}
	}
	return res
}

func ParseEnvelopeStruct(headers string) EnvelopeFields {
	fields := ParseEnvelope(headers)
	envelope := EnvelopeFields{
		To:      strings.Split(fields[HEADERTO], ","),
		From:    fields[HEADERFROM],
		Sender:  fields[HEADERSENDER],
		ReplyTo: fields[HEADERREPLYTO],
		Cc:      strings.Split(fields[HEADERCC], ","),
		Bcc:     strings.Split(fields[HEADERBCC], ","),
		Subject: fields[HEADERSUBJECT],
	}
	return envelope
}
