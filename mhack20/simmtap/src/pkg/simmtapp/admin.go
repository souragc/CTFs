package simmtapp

import (
	"fmt"
	"log"

	"github.com/spf13/cobra"
	"simmtapp/pkg/admin"
	"simmtapp/pkg/db"
)

var adminCMD = &cobra.Command{
	Use:   "admin",
	Short: "Starts admin script",
	Run:   adminRunner,
}

func adminRunner(cmd *cobra.Command, args []string) {
	var dbConn db.DB

	if err := dbConn.Connect(fmt.Sprintf("mongodb://%s", dbEndpoint)); err != nil {
		log.Fatal(err)
	}

	if err := dbConn.Init(); err != nil {
		log.Fatal(err)
	}

	admin.Execute(&dbConn)
}
