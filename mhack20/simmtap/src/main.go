package main

import (
	"log"

	"simmtapp/pkg/simmtapp"
)

func main() {
	err := simmtapp.Execute()
	if err != nil {
		log.Fatal(err)
	}
}
