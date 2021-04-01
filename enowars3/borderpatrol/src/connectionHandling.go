package main

import (
	"bufio"
	"bytes"
	"crypto/rand"
	"encoding/binary"
	"errors"
	"fmt"
	"math/big"
	"net"
	"os"
	"os/exec"
	"runtime/debug"
	"strconv"
	"time"
)

type state struct {
	protocol       string
	sequenceNumber int
	expectedPacket string
	memory         []byte
}

type session struct {
	inPackets     []packet
	outPackets    []packet
	inWindowSize  uint16
	outWindowSize uint16
	outQueue      [][]byte
	protocolState state
	key           []byte
	privileged    bool
}

func doNothing(p packet, s *session) error {
	return nil
}

func handleAWS(p packet, s *session) error {
	newSize := binary.BigEndian.Uint16(p.payload[0:2])
	if newSize < 8 || newSize > 512 || (newSize&(newSize-1)) != 0 {
		log("(E) [in handleAWS] Invalid Window Size", 2)
		return errors.New("Invalid Window Size")
	}
	s.inWindowSize = newSize

	log(fmt.Sprintf("(*) Adjusted Window Size: %d", newSize), 2)
	return nil
}

func handleGET(p packet, s *session) error {
	if !s.privileged {
		return errors.New("Unpriviliged")
	}
	reqType := string(p.payload[5:9])
	if reqType == "file" {
		file := string(p.payload[15:22])
		if file == "mem.bin" || file == "log.001" || file == "log.002" || file == "log.003" {
			logMutex.Lock()
			cmd := fmt.Sprintf("tar cvf - %s | xz > %s.tar.xz", file, file)
			exec.Command("bash", "-c", cmd).Output()
			f, err := os.OpenFile(fmt.Sprintf("%s.tar.xz", file), os.O_RDONLY, 0644)
			logMutex.Unlock()
			check(err)

			fs, err := f.Stat()
			check(err)
			fileSize := fs.Size()
			fmt.Println(fileSize)
			buf := make([]byte, fileSize)
			f.Read(buf)

			prepareEXP(s, uint32(fileSize))
			s.outQueue = append(s.outQueue, buf)
		}
		log(fmt.Sprintf("(*) Sent File: %s", file), 2)
	} else if reqType == "cert" {
		payload := make([]byte, 16)
		request := "cert_level=1&dbg=0"
		copy(payload, []byte(request))
		p := packet{[]byte("GET"), 16, payload, 1}
		raw := unpack(p)

		conn, err := net.Dial("tcp", fmt.Sprintf("[%s]:8888", CA))
		check(err)
		tmpReader := bufio.NewReader(conn)
		conn.Write(raw)
		buf := make([]byte, 8)
		_, err = tmpReader.Read(buf)
		check(err)

		prepareEXP(s, 8)
		s.outQueue = append(s.outQueue, buf)
	} else {
		return errors.New("Invalid Get Request")
	}

	return nil
}

func handleHCF(p packet, s *session) error {
	if !s.privileged {
		return errors.New("Unpriviliged")
	}
	fileInfo, err := os.Stat("mem.bin")
	if err == nil && time.Now().Sub(fileInfo.ModTime()).Seconds() < 30 {
		e := errors.New("HALT")
		check(e)
	}

	dumpMutex.Lock()
	os.Remove("mem.bin")
	f, err := os.OpenFile("mem.bin", os.O_CREATE|os.O_RDWR, 0644)
	check(err)
	fd := f.Fd()
	debug.WriteHeapDump(fd)
	f.Close()
	dumpMutex.Unlock()
	e := errors.New("HALT")
	check(e)
	return err
}

func handleLOG(p packet, s *session) error {
	if !s.privileged {
		return errors.New("Unpriviliged")
	}
	log(string(p.payload), 1)
	return nil
}

func handleZKP(p packet, s *session) error {
	log(fmt.Sprintf("(*) ZKP Step %d", s.protocolState.sequenceNumber), 2)
	switch sqn := s.protocolState.sequenceNumber; {
	case sqn == 0:
		prepareESQ(s, "ACC-ACC-ZKP(64)")
		s.protocolState.protocol = "ZKP"
		s.protocolState.memory = make([]byte, 128)
	case sqn%2 == 0:
		copy(s.protocolState.memory[0:64], p.payload[2:66])
		o, err := rand.Int(rand.Reader, big.NewInt(2))
		if err != nil {
			return errors.New("Bad Random Int")
		}
		copy(s.protocolState.memory[127:128], o.String())
		prepareZKP(s, []byte(fmt.Sprintf("disclose_option=%d", o)))
		s.protocolState.sequenceNumber++
	case sqn%2 != 0:
		o, err := strconv.Atoi(string(s.protocolState.memory[127:128]))
		if err != nil {
			return err
		}
		c := new(big.Int).SetBytes(s.protocolState.memory[0:64])
		if o == 0 {
			r := new(big.Int).SetBytes(p.payload[2:66])
			if new(big.Int).Exp(g, r, prime).Cmp(new(big.Int).Mod(c, prime)) != 0 {
				log("INCORRECT", 2)
				return errors.New("False")
			}
		} else {
			v := new(big.Int).SetBytes(p.payload[2:66])
			d := new(big.Int)
			new(big.Int).DivMod(new(big.Int).Mul(c, y), prime, d)
			if new(big.Int).Exp(g, v, prime).Cmp(d) != 0 {
				log("INCORRECT", 2)
				return errors.New("False")
			}
		}
		if sqn == 65 {
			prepareZKP(s, []byte("SUCCESS"))
			s.privileged = true
			s.protocolState.protocol = "FIN"
			log("[*] Entered Priviliged Mode", 1)
		} else {
			log("CORRECT", 2)
			prepareACC(s)
			s.protocolState.sequenceNumber++
		}
	default:
		return errors.New("Bad Sequence Number")

	}
	return nil
}

func prepareACC(s *session) {
	p := packet{[]byte("ACC"), s.outWindowSize, make([]byte, s.outWindowSize), 1}
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func prepareDNY(s *session) {
	p := packet{[]byte("DNY"), s.outWindowSize, make([]byte, s.outWindowSize), 1}
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func prepareAWS(s *session, size uint16) {
	p := packet{[]byte("AWS"), s.outWindowSize, make([]byte, s.outWindowSize), 1}
	binary.BigEndian.PutUint16(p.payload[0:2], size)
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outWindowSize = size
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func prepareESQ(s *session, sequence string) {
	if len(sequence) > int(s.outWindowSize) {
		log("(E) [in prepareESQ] Expected sequence does not fit in window size", 2)
		prepareDNY(s)
		return
	}
	payload := make([]byte, s.outWindowSize)
	copy(payload, []byte(sequence))
	p := packet{[]byte("ESQ"), s.outWindowSize, payload, 1}
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func prepareEXP(s *session, val uint32) {
	payload := make([]byte, s.outWindowSize)
	binary.BigEndian.PutUint32(payload[0:4], val)
	p := packet{[]byte("EXP"), s.outWindowSize, payload, 1}
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func prepareGET(s *session, request string) {
	payload := make([]byte, s.outWindowSize)
	copy(payload, []byte(request))
	p := packet{[]byte("GET"), s.outWindowSize, payload, 1}
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func prepareZKP(s *session, content []byte) {
	payload := make([]byte, s.outWindowSize)
	copy(payload, content)
	p := packet{[]byte("ZKP"), s.outWindowSize, payload, 1}
	raw := xorPacket(unpack(p), s)
	// raw := unpack(p)
	s.outQueue = append(s.outQueue, raw)
	s.outPackets = append(s.outPackets, p)
}

func handleConnection(c net.Conn) {
	defer func() {
		if r := recover(); r != nil {
			log(fmt.Sprintf("(X) Recovered from: %s", r), 1)
		}
	}()
	defer c.Close()
	bufReader := bufio.NewReader(c)

	currSession := session{[]packet{}, []packet{}, 16, 16, nil, state{}, generateKey(), false}
	currPacket := packet{}

	log("[+] New Connection", 1)

	timeoutShort := 3500 * time.Millisecond
	timeoutLong := 6 * time.Second
	c.SetReadDeadline(time.Now().Add(timeoutLong))

	for {
		buf := make([]byte, 12+currSession.inWindowSize)
		_, err := bufReader.Read(buf)
		check(err)
		currPacket, err = pack(xorPacket(buf, &currSession), &currSession)
		// currPacket, err = pack(buf, &currSession)
		if err != nil {
			bufReader.Reset(c)
			if len(currSession.outPackets) == 0 {
				log("(*) Send Session Key", 2)
				c.Write(currSession.key)
				c.SetReadDeadline(time.Now().Add(timeoutLong))
			} else {
				prepareDNY(&currSession)
			}
		} else {
			if bytes.Equal(currPacket.operation, []byte("CLS")) || len(currSession.inPackets) >= 256 {
				log("[-] Connection Closed", 1)
				return
			}
			err := OPCODES[string(currPacket.operation)].(func(packet, *session) error)(currPacket, &currSession)
			currSession.inPackets = append(currSession.inPackets, currPacket)

			bufReader.Reset(c)

			if currSession.protocolState.protocol != "" {
				if err != nil {
					prepareDNY(&currSession)
					log("DNY", 2)
					currSession.protocolState = state{}
				}
				if currSession.protocolState.protocol == "ZKP" {
					if tp := currSession.inPackets[len(currSession.inPackets)-1]; string(tp.operation) == "ACC" {
						if binary.BigEndian.Uint16(tp.payload[:2]) == 1 {
							currSession.protocolState.sequenceNumber++
							prepareAWS(&currSession, 256)
							currSession.inWindowSize = 256
						} else if binary.BigEndian.Uint16(tp.payload[:2]) == 2 {
							currSession.protocolState.sequenceNumber++
							prepareACC(&currSession)
						}
					}
				}
			} else if currSession.protocolState.protocol == "FIN" {
				currSession.protocolState = state{}
			} else {
				if err != nil {
					prepareDNY(&currSession)
					log("DNY", 2)
				} else {
					prepareACC(&currSession)
					log("ACC", 2)
				}
			}

			c.SetReadDeadline(time.Now().Add(timeoutShort))
		}

		if currSession.outQueue != nil {
			for _, p := range currSession.outQueue {
				c.Write(p)
			}
			currSession.outQueue = nil
		}
	}
}
