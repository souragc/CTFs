package main

import (
	"fmt"
	"regexp"
)

func flag_submit(flags string, io *Connection) {

	re := regexp.MustCompile("FAUST_[A-Za-z0-9/\\\\+]{32}")
	fl := re.FindAllStringSubmatch(flags, -1)

	for _, i := range fl {

		io.sendline(i[0])
		fmt.Print(io.recvline())
	}
}
