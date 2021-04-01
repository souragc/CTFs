from pwn import *

io = remote("challenges.tamuctf.com",31337)

i = 0

io.sendlineafter("bf$",",")

io.send("a")

#io.send("61"*5)

io.interactive()
