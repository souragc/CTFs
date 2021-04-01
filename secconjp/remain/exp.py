from pwn import *
io=process("./back",env={"LD_PRELOAD":"./libc.so.6_82d85352361acc81f202dc86292c1ca0fff3da3a"})
gdb.attach(io)
io.interactive()
