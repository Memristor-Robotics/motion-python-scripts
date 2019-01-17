#!/bin/python
import os
import io
import struct
import binascii
import time
os.system('stty -echo -parity raw 57600 -F/dev/serial0')

w = io.open("/dev/serial0", "wb")
r = io.open("/dev/serial0", "rb")


def crc(a):
	c = 0
		for i in a[2:]:
			c += ord(i)
		return ((~c) & 0xff)

def put_byte(id,addr,b):
	l = 4
	pkt= struct.pack('7B', 0xff, 0xff, id, l, 3, addr, b)
		pkt += struct.pack('B',crc(pkt))
		print(binascii.hexlify(pkt))
		#for i in range(256):
			#time.sleep(0.001)
			#w.write(pkt + struct.pack('B',i))   
			#w.write(pkt)
		w.write(pkt)
		w.flush()
	

def put_word(id,addr,v):
	l = 5
	pkt= struct.pack('6Bh', 0xff, 0xff, id, l, 3, addr, v)
		pkt += struct.pack('B',crc(pkt))
		print(binascii.hexlify(pkt))
		#for i in range(256):
			#w.write(pkt + struct.pack('B',i))   
			#w.write(pkt)
		w.write(pkt)
		w.flush()


def get(id,addr,b):
	l = 4
	pkt= struct.pack('7B', 0xff, 0xff, id, l, 2, addr, b)
		pkt += struct.pack('B',crc(pkt))
		print(binascii.hexlify(pkt))
		w.write(pkt)
		w.flush()
		print('reading: ')
		d=r.read(4)
		print('header: ' + binascii.hexlify(d))
		print(binascii.hexlify(r.read(255 - ord(d[3]))))
