from pwn import *
io=process("./main",env={"LD_PRELOAD":"./libc.so.6"})
io.interactive()
