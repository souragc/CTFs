package simmtapp

import (
	"fmt"
	"log"
	"net"
	"time"

	"github.com/spf13/cobra"
	"simmtapp/pkg/db"
	"simmtapp/pkg/imap"
)

var imapCMD = &cobra.Command{
	Use:   "imap",
	Short: "Starts imap server",
	Run:   imapRunner,
}

const defaultIMAPPort = 143

func imapRunner(cmd *cobra.Command, args []string) {
	if port == 0 {
		port = defaultIMAPPort
	}
	ln, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		log.Println(err)
		return
	}

	var dbConn db.DB
	err = dbConn.Connect(fmt.Sprintf("mongodb://%s", dbEndpoint))
	if err != nil {
		log.Fatal(err)
	}

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println(err)
			return
		}

		if err = conn.SetDeadline(time.Now().Add(alarmSeconds * time.Second)); err != nil {
			log.Println(err)
			return
		}

		go imap.HandleIMAPConnection(conn, &dbConn)
	}
}
