#!/usr/bin/python3

import tty
import os
import binascii
from convert import uchr

class Uart:
	def __init__(self):
		self.f = os.open("/dev/serial0", os.O_RDWR)
		#tty.setraw(self.f)
	
	def init():
		os.system('stty -echo raw 57600 -F/dev/serial0')
		
	def rddata(self, n=1):
		b = b''
		while n > 0:
			d = os.read(self.f, 1)
			n -= len(d)
			b += d
		return b

	
	# SCTLxxxx
	def read(self):
		sync = 0x3c
		while True:
			S = self.rddata()[0]
			if S == sync:
				C = self.rddata()[0]
				T = self.rddata()[0]
				L = self.rddata()[0]

				#print("reading " + hex(C) + " " + hex(T) + " " + hex(L) )
				CH = C >> 4
				CP = C & 0xf

				if CH != ((T + L) & 0xf):
					continue

				#print("header ok")
				c = 0
				data = self.rddata(L)
				for i in data:
					c += i

				if CP != (c & 0xf):
					continue
				return (T, data)


	def send(self, x):
		binary = x
		#print('bin: ' , binascii.hexlify(binary))
		ptype = binary[0]
		payload = len(binary)-1
		header_checksum = (ptype + payload) & 0xf
		payload_checksum = 0
		for i in binary[1:]:
			payload_checksum += i
		payload_checksum &= 0xf
		checksum = (header_checksum << 4) | payload_checksum

		packet = b'\x3c' + uchr(checksum) + uchr(ptype) + uchr(payload) + binary[1:]
		print(binascii.hexlify(packet))
		os.write(self.f, packet)

