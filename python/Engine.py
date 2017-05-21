from math import sqrt

from convert import *
from conf import *
from const_motion import *
from parser import *
from const_motion import *

status_idle = 'I'

def vec_length(x,y):
	return sqrt(x**2+y**2)
		
class Engine:
	def __init__(self):
		self.debug = 0
		self.point = [1,2]
		self.tol = 40
		self.addr = motion_can_addr
		self.use_can = use_can
		if use_can == 1:
			from Can import Can
			self.com = Can()
		else:
			from Uart import Uart
			self.com = Uart()
	def wait_for_arrival(self):
		while True:
			pkt = read()
			p = pkt[1]
			if chr(pkt[0]) == 'p':
				#print("pkt p: ", pkt[1])
				P_cmd(pkt[1])
				x = l16(p,1)
				y = l16(p,3)
				o = l16(p,5)
				s = l16(p,7)
				if tol > 0 and vec_length(x-point[0], y-point[1]) < tol:
					print("tolerance done")
					return True
				
			elif chr(pkt[0]) == 'P':
				#print("pkt P: ", pkt[1])
				P_cmd(pkt[1])
				if p[0] == status_idle:
					print("idle, done")
					return True
			else:
				if debug:
					print("pkt: ", chr(pkt[0]))
	
	
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
						tokens[j] = chr(int(i[0:2], 16)) + i[2:]
					else:
						tokens[j] = chr(int(i[0], 16)) + i[1:]
			binary = (''.join(tokens)).encode('latin1')
		else:
			binary = x
		
		if self.use_can:
			self.com.send(binary, self.addr)
		else:
			self.com.send(binary)
					
	def read(self):
		if self.use_can:
			frm = self.com.read(self.addr)
			return (frm[0], frm[1:])
		else:
			return self.com.read()
		
	def move_to_cmd(self, x,y,r=100,o=1):
		self.send(b'N' + pack(x) + pack(y) + uchr(to_uchar(o)) + pack(r))
		
	def goto_cmd(self, x,y,r=100,o=1):
		self.send(b'G' + pack(x) + pack(y) + uchr(to_uchar(o)))
		
	def turn_cmd(self, o):
		self.send(b'T' + pack(o))
		
	def speed(self, s):
		self.send(b'V' + uchr(s))
		
	def intr(self):
		self.send(b'i')
		
	def move(self, x,y,r=100,o=1):
		print('moving to: ', x, y)
		self.intr()
		point = [x,y]
		self.move_to_cmd(x,y,r,o)
		self.wait_for_arrival()

	def goto(self, x,y,o=1):
		print('goto: ', x, y)
		self.intr()
		point = [x,y]
		self.goto_cmd(x,y,o)
		self.wait_for_arrival()

	def turn(self, o):
		print('turn: ', o)
		self.intr()
		self.turn_cmd(o)
		self.wait_for_arrival(0)
		
	def setpos(self, x,y,o=0):
		self.send(b'I' + pack(x) + pack(y) + pack(o))


	def conf_list(self):
		print('bytes: ', config_bytes)
		print('ints: ', config_ints)
		print('floats: ', config_floats)

	def conf_get_key(self, c):
		if c in config_bytes:
			return config_bytes.index(c)
		elif c in config_ints:
			return config_ints.index(c) + len(config_bytes)
		elif c in config_floats:
			return config_floats.index(c) + len(config_bytes) + len(config_ints)
		else: 
			return False

	def conf_set(self, c,v):
		if c in config_ints:
			self.send(b'c' + uchr(len(config_bytes) + config_ints.index(c)) + pack32(int(v) << 4))
		elif c in config_bytes:
			self.send(b'c' + uchr(config_bytes.index(c)) + pack32(int(v) << 4))
		elif c in config_floats:
			self.send(b'c' + uchr(len(config_bytes) + len(config_ints) + config_floats.index(c)) + float_to_uint32(float(v), 4))    
		else:
			return False
		return True

	def conf_get(self, c):
		self.send(b'C' + uchr(self.conf_get_key(c)))
		while True:
			p = self.read()
			print(p)
			if p[0] == b'C'[0] and len(p[1]) >= 4:
				return uint32_to_float(struct.unpack('>I',p[1])[0])  

