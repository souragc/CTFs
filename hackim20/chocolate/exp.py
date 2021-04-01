from pwn import *
import hashlib
import string

stri = "abcdefghijklmnopqrstuvwxyzWOERFJASKL"
io=remote("pwn3.ctf.nullcon.net",1234)
io.recvuntil('sha256("')
str1 = io.recvuntil('"').strip('"')
io.recvuntil('startswith("')
str2 = io.recvuntil('"').strip('"')
log.info("str1 = " + str(str1))
log.info("str2 = " + str(str2))
res = ""
f = 0
for i in stri:
    for j in stri:
        for k in stri:
            for l in stri:
                str0 = (i)+(j)+(k) + l
                result = hashlib.sha256(str1+str0)
                if(result.hexdigest().startswith(str2)):
                    print str0
                    log.info("str = " + str(str0))
                    res = str0
                    f = 1
                    io.sendlineafter("length 3\n",res)
                    break
                    io.interactive()
                    break
                if(f==1):
                    break
            if(f==1):
                break
        if(f==1):
            break
    if(f==1):
        break

io.recvuntil("hello\n")
io.interactive()
