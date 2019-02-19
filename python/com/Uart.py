#!/usr/bin/python3

import tty,os,binascii,time
from conf import *
from util.Convert import *
import serial

class Uart:
	def __init__(self):
		self.f = serial.Serial(uart_dev, 57600)
	
	def init():
		os.system('stty -echo raw '+str(uart_baud)+' -F'+uart_dev)
		
	def rddata(self, n=1):
		b = b''
		while n > 0:
			try:
				d = self.f.read(n)
			except:
				continue
			n -= len(d)
			b += d
		return b
	
	# SCTLxxxx
	def read(self, addr=None):
		sync = 0x3c
		while True:
			S = self.rddata()[0]
			if S == sync:
				#  print('msg ' + str(S))
				C = self.rddata()[0]
				T = self.rddata()[0]
				L = self.rddata()[0]

				CH = C >> 4
				CP = C & 0xf

				if CH != ((T + L) & 0xf):
					print('header checksum bad')
					continue
				c = 0
				data = self.rddata(L)
				for i in data: c += i
				if CP != (c & 0xf):
					print('data checksum bad')
					continue
				return (T, data)
			else:
				print('not sync: ' + hex(S))

	def flush(self): self.f.flushInput()
	
	def send(self, x, addr=None):
		binary = x
		ptype = binary[0]
		payload = len(binary)-1
		header_checksum = (ptype + payload) & 0xf
		payload_checksum = 0
		for i in binary[1:]: payload_checksum += i
		payload_checksum &= 0xf
		checksum = (header_checksum << 4) | payload_checksum
		packet = b'\x3c' + p8(checksum) + p8(ptype) + p8(payload) + binary[1:]
		# print(binascii.hexlify(packet))
		self.f.write(packet)
		time.sleep(0.11)

