package main

import (
	"math/big"
	"net"
	"sync"
)

const (
	HOST  = "[::]"
	PORT  = "41314"
	CA    = "borderpatrol.enowars.com"
	DEBUG = true
)

var g, _ = new(big.Int).SetString("2", 10)
var prime, _ = new(big.Int).SetString("7211120725388770757449064920117053258626350409292518732487977076334774457178724668781927073094705280276788047107026280406597259439312993043207548964593709", 10)
var y, _ = new(big.Int).SetString("3791681507150338158995503145950387058281565872405011862192137930605710794447294645064985636919183844757477896341909957083567025441343602771513168204170391", 10)

var dumpMutex = &sync.Mutex{}
var logMutex = &sync.Mutex{}

func main() {
	l, err := net.Listen("tcp", HOST+":"+PORT)
	check(err)
	defer l.Close()

	for {
		conn, err := l.Accept()
		check(err)
		go handleConnection(conn)
	}
}
