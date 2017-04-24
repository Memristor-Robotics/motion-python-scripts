from uart import *
from const import *
from convert import *
import struct

def conf_list():
    print('bytes: ', config_bytes)
    print('ints: ', config_ints)
    print('floats: ', config_floats)

def conf_get_key(c):
    if c in config_bytes:
        return config_bytes.index(c)
    elif c in config_ints:
        return config_ints.index(c) + len(config_bytes)
    elif c in config_floats:
        return config_floats.index(c) + len(config_bytes) + len(config_ints)
    else: 
        return False

def conf_set(c,v):
    if c in config_ints:
        send('c' + chr(len(config_bytes) + config_ints.index(c)) + pack32(int(v) << 4))
    elif c in config_bytes:
        send('c' + chr(config_bytes.index(c)) + pack32(int(v) << 4))
    elif c in config_floats:
        send('c' + chr(len(config_bytes) + len(config_ints) + config_floats.index(c)) + float_to_uint32(float(v), 4))    
    else:
        return False
    return True

def conf_get(c):
    send('C' + chr(conf_get_key(c)))
    while True:
        p = read()
        if chr(p[0]) == 'C' and len(p[1]) >= 4:
            return uint32_to_float(struct.unpack('>I',p[1])[0])  
