from pwn import *

io = process("./still-printf",env={"LD_PRELOAD":"./libc-2.28.so"})

gdb.attach(io)

io.sendline("aaa")
io.interactive()
