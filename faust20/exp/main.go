package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"os"
	"os/exec"
	"strconv"
	"sync"
)

func main() {

	args := os.Args[1:]
	if len(args) != 2 {

		fmt.Println("Usage: ", os.Args[0], " FILE ", " IP_LIST ")
		os.Exit(0)

	}

	file := args[0]

	if !fileExists(file) {
		fmt.Println(file, " does not exist")
		os.Exit(0)

	}

	jdata, err := ioutil.ReadFile(args[1])

	if err != nil {

		fmt.Println(err)
	}

	ip_list := team_list(jdata)

	io, err := remote("submission.faustctf.net", 666)

	connFlag := 0

	if err != nil {

		fmt.Println("Connection to Flag Submission server not established so writing files to /tmp/CTFflags")

		connFlag = 1
		log.Println(err)

	}

	f, err := os.OpenFile("/tmp/CTFflags",
		os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Println(err)
	}

	var wg sync.WaitGroup
	wg.Add(len(ip_list))

	for _, ip := range ip_list {

		go func(ip string) {

			defer wg.Done()
			// take the ip_address as command line argument
			cmd := exec.Command("python", file, ip)

			out, err := cmd.CombinedOutput()

			if err != nil {

				fmt.Println("Error: ", err, "for ip: ", ip)

			}

			// If connection to flag submitter is now working then write files to /tmp/CTFflags
			if connFlag == 0 {
				flag_submit(string(out), &io)

			} else {

				if _, err := f.WriteString(string(out)); err != nil {
					log.Println(err)
				}
			}

		}(ip)
	}

	wg.Wait()

}

// To check if file exists
func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

// Utility Functions
// Connection stores all the details regarding an active Connction
type Connection struct {
	reader     *bufio.Reader
	writer     *bufio.Writer
	connection net.Conn
}

func remote(ip string, port int) (Connection, error) {
	addr := ip + ":" + strconv.Itoa(port)
	connection, err := net.Dial("tcp", addr)
	if err != nil {
		log.Printf("Unable to Connect to : %s -> %v", addr, err)
		return Connection{
			reader:     bufio.NewReader(connection),
			writer:     bufio.NewWriter(connection),
			connection: connection,
		}, err
	}
	return Connection{
		reader:     bufio.NewReader(connection),
		writer:     bufio.NewWriter(connection),
		connection: connection,
	}, err
}

func (io Connection) sendline(str string) (int, error) {
	count, err := io.writer.WriteString(str + "\n")
	io.writer.Flush()
	return count, err
}

func (io Connection) recvline() ([]byte, error) {

	out, err := io.readuntil("\n")

	if err != nil {

		return nil, err

	}

	return out, err

}

func (io Connection) readuntil(until string) ([]byte, error) {
	consume := until
	flag := false
	var out []byte
	for {
		res, err := io.reader.ReadBytes(consume[0])
		if err != nil {
			return nil, err
		}

		if flag {
			if len(res) != 1 {
				consume = until
			} else {
				consume = consume[1:]
			}
		} else {
			flag = true
			consume = consume[1:]
		}
		out = append(out, res...)
		if len(consume) == 0 {
			break
		}
	}
	return out, nil
}
