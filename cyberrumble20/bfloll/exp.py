from pwn import *
io = process("./bflol")

gdb.attach(io)
payload = ".."
io.sendline(payload)
io.interactive()
