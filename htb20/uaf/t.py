from pwn import *
io = process("./a.out",env={"LD_PRELOAD":"./libc.so.6"})
gdb.attach(io)
io.interactive()
