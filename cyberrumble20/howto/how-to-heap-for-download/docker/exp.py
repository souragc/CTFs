from pwn import *
io = process("./howtoheap",env={"LD_PRELOAD":"./libc-2.32.so"})
io.interactive()
