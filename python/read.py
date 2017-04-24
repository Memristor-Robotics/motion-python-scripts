#!/usr/bin/python


import sys
import io

r = io.open("/dev/serial0", "rb")

sync = 0x3c
# SCTLxxxx
def read():
    while True:
        S = ord(r.read(1))
        if S == sync:
            C = ord(r.read(1))
            T = ord(r.read(1))
            L = ord(r.read(1))

            #print("reading " + hex(C) + " " + hex(T) + " " + hex(L) )
            CH = C >> 4
            CP = C & 0xf

            if CH != ((T + L) & 0xf):
                continue

            #print("header ok")
            c = 0
            data = r.read(L)
            for i in data:
                c += ord(i)

            if CP != (c & 0xf):
                continue
            #print("data ok")
            return (T, data)


