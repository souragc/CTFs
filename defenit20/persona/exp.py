from pwn import *
import hashlib

def solve_pow(check):
    for k in range(255):
        for j in range(255):
            for i in range(255):
                strr = str(i)+str(j)+str(k)
                result = hashlib.sha256(strr.encode())
                result = result.hexdigest()
                if(result[-6:]==check):
                    return str(i)+str(j)+str(k)

io = remote("persona.ctf.defenit.kr", 9999)
leak = io.recvuntil("str : ").split("\n")[0].split('"')[1]
io.sendline(solve_pow(leak))
io.interactive()
