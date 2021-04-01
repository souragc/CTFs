package main

import (
	"bytes"
	"encoding/binary"
	"errors"
)

var OPCODES = map[string]interface{}{
	"ACC": doNothing, // Accept
	"AWS": handleAWS, // Adjust Window Size
	"CLS": doNothing, // Close
	"DNY": doNothing, // Deny
	"EXP": doNothing, // Expect Bytes
	"ESQ": doNothing, // Expect Sequence
	"GET": handleGET, // Get Resource
	"HCF": handleHCF, // Halt and Catch Fire
	"KEX": doNothing, // Key Exchange
	"LOG": handleLOG, // Log Comment
	"ZKP": handleZKP, // Zero Knowledge Proof Protocol
}

type packet struct {
	operation      []byte
	windowSize     uint16
	payload        []byte
	privilegedByte byte
}

func pack(raw []byte, s *session) (packet, error) {
	header := raw[0:4]
	pBit := raw[len(raw)-1]
	if len(raw) != 12+int(s.inWindowSize) || !bytes.Equal(header, []byte("ENO/")) || raw[7] != byte('/') ||
		raw[10] != byte('/') || (pBit != byte('\x00') && pBit != byte('\x01')) {
		log("(E) [in pack:1] Invalid Packet", 2)
		return packet{}, errors.New("Invalid Packet")
	}
	op := raw[4:7]

	found := false
	for c, _ := range OPCODES {
		if bytes.Equal([]byte(c), op) {
			found = true
		}
	}

	size := binary.BigEndian.Uint16(raw[8:10])
	if !found || size != s.inWindowSize || size < 8 || size > 512 {
		log("(E) [in pack:2] Invalid Packet", 2)
		return packet{}, errors.New("Invalid Packet")
	}

	payload := raw[11 : 11+size]

	newPacket := packet{op, size, payload, pBit}
	return newPacket, nil
}

func unpack(p packet) []byte {
	totalSize := 12 + p.windowSize
	raw := make([]byte, totalSize)

	copy(raw[0:4], []byte("ENO/"))
	copy(raw[4:7], p.operation)
	copy(raw[7:8], []byte("/"))
	binary.BigEndian.PutUint16(raw[8:10], p.windowSize)
	copy(raw[10:11], []byte("/"))
	copy(raw[11:11+p.windowSize], p.payload)
	copy(raw[len(raw)-1:], append(make([]byte, 1), p.privilegedByte))

	return raw
}

func xorPacket(input []byte, s *session) (output []byte) {
	for i := 0; i < len(input); i++ {
		output = append(output, input[i]^s.key[i%len(s.key)])
	}

	return output
}
