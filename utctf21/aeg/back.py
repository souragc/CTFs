from pwn import *

io=remote("pwn.utctf.live",9997)
io.sendlineafter("Press enter when you're ready for the first binary.\n",'\n')
f = io.recvuntil("You")
log.info("f = " + str(f)[:-3])
with open("out2","w+") as fp:
    fp.writelines(f[:-3])
os.system("cat out2 | xxd -r > bin2".format(f))
