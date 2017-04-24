#!/usr/bin/python

import tty
import os

f = os.open("/dev/serial0", os.O_RDWR)

tty.setraw(f)

bdata = ''
def chdata(n=1):
    global bdata
    if len(bdata) >= n:
        return True
    d = os.read(f,n-len(bdata))
    bdata += d
    if len(bdata) >= n:
        return True
    return False


def rddata(n=1):
    global bdata
    if len(bdata) >= n:
        data = bdata[:n]
        bdata = bdata[n:]
        return data
    
    n -= len(bdata)
    while n > 0:
        d = os.read(f, n)
        n -= len(d)
        bdata += d
    data = bdata
    bdata = ''
    return data

sync = 0x3c
# SCTLxxxx
def read():
    while True:
        S = ord(rddata())
        if S == sync:
            C = ord(rddata())
            T = ord(rddata())
            L = ord(rddata())

            #print("reading " + hex(C) + " " + hex(T) + " " + hex(L) )
            CH = C >> 4
            CP = C & 0xf

            if CH != ((T + L) & 0xf):
                continue

            #print("header ok")
            c = 0
            data = rddata(L)
            for i in data:
                c += ord(i)

            if CP != (c & 0xf):
                continue
            return (T, data)


def send(x, process=False):
    text = x
    if process:
        tokens = text.split("\\x")
        def ishex(x):
            return (x >= '0' and x <= '9') or (x >= 'a' and x <= 'f')

        for j in range(1, len(tokens)):
            i = tokens[j]
            if len(i) == 0: continue
            if ishex(i[0].lower()):
                if len(i) >= 2 and ishex(i[1].lower()):
                    tokens[j] = '' + chr(int(i[0:2], 16)) + i[2:]
                else:
                    tokens[j] = chr(int(i[0], 16)) + i[1:]
       
        binary = ''.join(tokens)
    else:
        binary = text
    ptype = binary[0]
    payload = len(binary)-1
    header_checksum = (ord(ptype) + payload) & 0xf
    payload_checksum = 0
    for i in binary[1:]:
        payload_checksum += ord(i)
    payload_checksum &= 0xf
    checksum = chr((header_checksum << 4) | payload_checksum)

    packet = '\x3c' + checksum + ptype + chr(payload) + binary[1:]

    os.write(f, packet)

