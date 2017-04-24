
import struct
def float_to_uint32(x, decimals=4):
    x *= pow(10, decimals & 0xf)
    x = int(x)
    return pack32((x << 4) | decimals & 0xf)

def uint32_to_float(x):
    return float(x >> 4) / pow(10, x & 0xf)

def to_uint16(x):
    if x < 0:
        x = x + 2**16
    return x

def to_int16(x):
    if x > 2**15:
        x = x - 2**16
    return x

def to_uchar(x):
    if x < 0:
        x = x + 2**8
    return x

def cx(x):
    return hex(c(x))


def l16(x, idx):
    return to_int16( (ord(x[idx]) << 8) | ord(x[idx+1]) );

def ls16(x, idx):
    return str(l16(x,idx))

def pack32(x):
    return str(struct.pack('>i', x))
def pack(x):
    return str(struct.pack('>h', x))
