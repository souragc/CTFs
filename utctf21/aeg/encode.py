from pwn import *
io = process("./bin1")

#arr = "aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnoooopppp"
arr = "hhhhiiiijjjjkkkkllllmmmmnnnnooooppppqqqqrrrrssssttttuuuuvvvvwwww"


def split():
    global arr
    arr=  [char for char in arr] 

def stage7(payload, val):
    out = []
    for i in range(val, 64+val):
        out.append(payload[i%64])
    return "".join(out)

def stage6(payload, grouping2):
    newarr = [0]*64
    for i in range(16):
        for j in range(4):
            newarr[grouping2[i]*4 + j] = payload[i*4 + j]
    return "".join(newarr)

def stage5(payload, val):
    out = []
    for i in range(64):
        out.append(chr((ord(payload[i]) - val) % 255))
    return "".join(out)

def stage4(payload, val):
    out = []
    for i in range(64):
        out.append(chr(ord(payload[i])^val))
    return "".join(out)

def stage3(payload, val):
    return stage7(payload, val)

def stage2(payload, grouping1):
    newarr = [0]*64
    for i in range(16):
        for j in range(4):
            newarr[grouping1[i]*4 + j] = payload[i*4 + j]
    return "".join(newarr)

def stage1(payload, val):
    return stage4(payload, val)

def decrypt(payload):
    grouping1 = [5, 9, 0, 0xa, 7, 0xd, 8, 3, 2, 6, 0xc, 4, 0xf, 0xe, 0xb, 1]
    grouping2 = [0xe, 0, 3, 1, 9, 0xf, 6, 0xb, 4, 0xa, 8, 2, 7, 0xd, 5, 0xc]
    payload = stage7(payload, 47)
    payload = stage6(payload, grouping2)
    payload = stage5(payload, 114)
    payload = stage4(payload, 0xdc)
    payload = stage3(payload, 44)
    payload = stage2(payload, grouping1)
    return stage1(payload, 0xf9)

split()
gdb.attach(io)
io.send(decrypt(arr))
io.interactive()
