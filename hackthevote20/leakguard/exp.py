from pwn import *

io=process("./candles",env={"LD_PRELOAD":"./leakguard.so"})
gdb.attach(io)
io.interactive()
