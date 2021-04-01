from pwn import *
io=process("./back",env={"LD_PRELOAD":"./libc.so.6"})

io.sendlineafter("Enter your name: ","aaaaaa")

def open_main():
    io.sendlineafter("> ","1")

def read_main():
    io.sendlineafter("> ","2")

def close_main():
    io.sendlineafter("> ","3")

def create_sub(option,name=""):
    io.sendlineafter("> ","4")
    io.sendlineafter("{?} Do you agree with this name?[Y\N]: ",option)
    if(option=="N"):
        io.sendlineafter("{?} Enter your name: ",name)


def write_sub(name):
    io.sendlineafter("> ","5")
    io.sendafter("{?} Enter data: ",name)

def read_sub():
    io.sendlineafter("> ","6")

def close_sub():
    io.sendlineafter("> ","7")

def change_user(name):
    io.sendlineafter("> ","8")
    io.sendlineafter("{?} Enter new username: ",name)

#open_main()
#create_sub("Y")
#write_sub("a"*0x600)
#read_sub()
#out=u32(io.recvuntil("------")[-10:-6])
#print hex(out)


gdb.attach(io)

io.interactive()
