from pwn import *

io = process("./mmap_clone_3_cat 50505")
io.interactive()
