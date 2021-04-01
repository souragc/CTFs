package simmtapp

import (
	"fmt"
	"log"
	"net"
	"time"

	"github.com/spf13/cobra"
	"simmtapp/pkg/db"
	"simmtapp/pkg/smtp"
)

var smtpCMD = &cobra.Command{
	Use:   "smtp",
	Short: "Starts smtp server",
	Run:   smtpRunner,
}

const defaultSMTPPort = 25

func smtpRunner(cmd *cobra.Command, args []string) {
	var dbConn db.DB

	err := dbConn.Connect(fmt.Sprintf("mongodb://%s", dbEndpoint))
	if err != nil {
		log.Fatal(err)
	}

	if port == 0 {
		port = defaultSMTPPort
	}
	ln, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println(err)
		} else {
			if err = conn.SetDeadline(time.Now().Add(alarmSeconds * time.Second)); err != nil {
				log.Println(err)
			} else {
				go smtp.HandleSMTPConnection(conn, &dbConn)
			}
		}
	}
}
