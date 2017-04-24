

import io
import sys
import struct

w = io.open("/dev/serial0", "wb")
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

    #print(" ".join("{:02x} ".format(ord(c)) for c in packet))
    w.write(packet)


def pack32(x):
    return str(struct.pack('>i', x))
def pack(x):
    return str(struct.pack('>h', x))
