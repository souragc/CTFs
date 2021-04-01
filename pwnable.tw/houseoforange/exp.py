from pwn import *
io=process("./houseoforange",env={"LD_PRELOAD":"./libc.so.6"})
io.interactive()
