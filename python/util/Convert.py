
import struct, binascii
from math import log10

# conversions
def to_uint8(x): return x + 2**8 if x < 0 else x
def to_uint16(x): return x + 2**16 if x < 0 else x
def to_uint32(x): return x + 2**32 if x < 0 else x
def to_int8(x): return x - 2**7 if x > 2**7 else x
def to_int16(x): return x - 2**16 if x > 2**15 else x
def to_int32(x): return x - 2**32 if x > 2**31 else x
# packing
def p8(x): return bytes([x + 2**8 if x < 0 else x])
def p32(x): return struct.pack('>i', x)
def p16(x): return struct.pack('>H', to_uint16(x))
# loading
def l8(x, idx): return x[idx]
def l16(x, idx): return struct.unpack('>h', x[idx:idx+2])[0]
def l32(x, idx): return struct.unpack('>i', x[idx:idx+4])[0]


def nice_hex(s, spaces=4):
		h = binascii.hexlify(s).decode('ascii')
		return ' '.join([h[i:i+spaces] for i in range(0, len(h)-(len(h)%spaces)+spaces, spaces)])

