from pwn import *
io=process("./copy",env={"LD_PRELOAD":"./libc-2.27.so"})
gdb.attach(io)
io.interactive()
