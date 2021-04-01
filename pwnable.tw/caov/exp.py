from pwn import *
import ctypes

io = process("./caov")

#name = "aaaaa"
#io.sendlineafter("Enter your name: ",name)

#key = "bbbb"
#io.sendlineafter("Please input a key: ",str(key))


#gdb.attach(io)
#value = 10
#io.sendlineafter("Please input a value: ",str(value))

io.interactive()
