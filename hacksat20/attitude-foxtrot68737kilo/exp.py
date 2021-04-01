from pwn import *

catalog = []
input_set = []

def get_X(ind):
    return catalog[ind][0]

def get_Y(ind):
    return catalog[ind][1]

def get_Z(ind):
    return catalog[ind][2]

def get_mag(ind):
    return catalog[ind][3]

def b2s(a):
    return "".join(list(map(chr, a)))

def auth():
    r.recv()
    r.sendline("ticket{foxtrot68737kilo:GGDoopQoWpKtvYSUqjZ7MlR3FlePvQLxp8p9B5ZpkSr40FMSYoBhRIuT9puMOC60mg}")

def read_catalog():
    data = open("test.txt").readlines()
    for line in data:
        val = [x.strip() for x in line.split(",")]
        catalog.append(val)

def read_input():
    r.recvuntil(b"--\n")
    data = b2s(r.recvuntil(b"\n\n").strip())
    lines = data.split("\n")
    for line in lines:
        idx = int(line.split(":")[0].strip())
        cords = list(map(float, [x.strip() for x in line.split(":")[1].split(",")]))
        input_set.append((idx, cords))
    #print(r.recvuntil(b"%f\n"))

def main():
    read_catalog()
    auth()
    read_input()
    print(input_set)
    r.interactive()

if __name__ == "__main__":
    r  = remote('attitude.satellitesabove.me', 5012)
    main()
