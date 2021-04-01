package main

import (
	"bytes"
	"crypto/rand"
	"fmt"
	"os"
	"runtime"
	"time"
)

var lastLogRotateTime = time.Now().UTC()
var currLogfile = "log.001"

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func getGID() string {
	b := make([]byte, 64)
	b = b[:runtime.Stack(b, false)]
	b = bytes.TrimPrefix(b, []byte("goroutine "))
	b = b[:bytes.IndexByte(b, ' ')]
	return string(b)
}

func log(msg string, level int) {
	if !DEBUG && level == 2 {
		return
	}
	t := (time.Now().UTC()).Format("2006-01-02 15:04:05.000")
	logline := fmt.Sprintf("[LOG] {%03s} [%s] %s\n", getGID(), t, msg)
	fmt.Println(logline)

	if level == 1 {
		currTime := time.Now().UTC()
		logMutex.Lock()
		if currTime.Sub(lastLogRotateTime).Seconds() > 270 {
			lastLogRotateTime = currTime
			if currLogfile[6] == '1' {
				currLogfile = "log.002"
			} else if currLogfile[6] == '2' {
				currLogfile = "log.003"
			} else if currLogfile[6] == '3' {
				currLogfile = "log.001"
			}
			os.Remove(currLogfile)
		}
		f, err := os.OpenFile(currLogfile, os.O_CREATE|os.O_APPEND|os.O_RDWR, 0644)
		check(err)
		f.Write([]byte(logline))
		f.Close()
		logMutex.Unlock()
	}
}

func generateKey() []byte {
	raw := make([]byte, 32)
	_, err := rand.Read(raw)
	check(err)
	return raw
}
