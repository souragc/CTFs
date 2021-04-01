from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc.so.6"})

io.interactive()
