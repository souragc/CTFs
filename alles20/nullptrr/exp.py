from pwn import *

io = process("./a.out")
gdb.attach(io)
io.sendline(p64(0xdeadbeef))
io.interactive()
