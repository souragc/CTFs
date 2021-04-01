from pwn import *

io = process("./rrop")

io.interactive()
