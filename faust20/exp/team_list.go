package main

import (
	"encoding/json"
	"fmt"
)

func team_list(data []byte) []string {

	// change variable result according to the structure of the team json
	var result map[string][]string
	err := json.Unmarshal(data, &result)
	if err != nil {
		fmt.Println(err)
	}

	return result["teams"]
}
