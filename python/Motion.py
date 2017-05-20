

import io
import sys
import struct

class Motion:
	def __init__(self, use_can=True):
		if use_can:
			import cansend
			self.c = cansend.mycan()
			self.addr = 600
			self.use_can = True
		else:
			import uart
			self.c = Uart()
			self.use_can = False
		
	def send(self, x, process=False):
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
		
		if self.use_can:
			binary = str.encode(binary)
			self.c.send(self.addr, binary)
		else:
			self.c.send(binary)

	def read(self, addr=None):
		if self.use_can:
			binary = str.encode(binary)
			pkt = self.c.recv(self.addr)
			t = ord(pkt[0])
			return (t, pkt[1:])
		else:
			return self.c.read()
