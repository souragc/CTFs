package simmtapp

import (
	"github.com/spf13/cobra"
)

var (
	rootCmd = &cobra.Command{
		Use:   "simmtapp",
		Short: "An IMAP and SMTP capable mail server",
		Long:  `SiMmTaPp is a powerful, secure, full-fledged, scalable, multi-user modern mail server`,
	}
	port       int
	dbEndpoint string
)

const alarmSeconds = 60

func Execute() error {
	return rootCmd.Execute()
}

func init() {
	rootCmd.PersistentFlags().IntVarP(&port, "port", "p", 0, "tcp port")
	rootCmd.PersistentFlags().StringVarP(&dbEndpoint, "db-endpoint", "d", "db:27017", "database host and port: '<host>:<port>'")
	rootCmd.AddCommand(imapCMD, smtpCMD, adminCMD)

}
