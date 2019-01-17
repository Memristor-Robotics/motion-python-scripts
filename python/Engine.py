import sys
sys.dont_write_bytecode = True
from math import sqrt,modf
from util.Convert import *
from conf import *

status_idle = 'I'
def simple_hash(v):
	h=5381
	for i in v: h = h*33 + ord(i)
	return int(h) & 0xffff

def vec_length(x,y): return sqrt(x**2+y**2)

class Engine:
	def __init__(self, _use_can=None, can_addr=motion_can_addr, dont_stop_on_exit=False):
		self.debug = 0
		self.point = [1,2]
		self.tol = 0
		self.addr = can_addr
		self.use_can = _use_can if _use_can != None else use_can
		self.use_hash=use_hash
		
		if self.use_can == 1:
			from com.Can import Can
			self.com = Can()
			self.servo = self.com.servo
			self.actuator = self.com.actuator
		else:
			from com.Uart import Uart
			self.com = Uart()
		
		# stop robot on ctrl-c
		def on_interrupt(a,b):
			if not dont_stop_on_exit:	
				self.stop()
			exit(0)
		import signal
		signal.signal(signal.SIGINT, on_interrupt)
		
	def wait_for_N(self):
		while True:
			pkt = self.read()
			if chr(pkt[0]) == 'N': return True
		return True
		
	def wait_for_arrival(self):
		cycle=0
		trans=0
		idles=0
		n_idles = 5
		while True:
			pkt = self.read()
			p = pkt[1]
			if chr(pkt[0]) == 'P':
				x = l16(p,1)
				y = l16(p,3)
				o = l16(p,5)
				if self.tol > 0 and vec_length(x-self.point[0], y-self.point[1]) < self.tol:
					print('resolved with tolerance')
					return True
				
			if chr(pkt[0]) in ['N', 'E', 'S']: return True
			if chr(pkt[0]) == 'p' and chr(p[0]) == 'I': return True
	
	def send(self, msg, addr=None, process_bash_input=False):
		binary=msg if not process_bash_input else eval('"'+msg+'"')
		if type(binary) is not bytes: binary=binary.encode()
		if self.debug: print(nice_hex(binary))
		self.com.send(binary, addr if addr != None else self.addr)
	
	def read(self):
		frm = self.com.read(self.addr)
		return (frm[0], frm[1:]) if self.use_can else frm
		
	
	def print_cmd(self, name, *args):
		print('\x1b[33m',name+':','\x1b[0m', *args)
	
	####### RAW COMMANDS #######
	def move_cmd(self, x,y,r=100,dir=1): self.send(b'N' + p16(x) + p16(y) + p16(r) + p8(dir))
	def goto_cmd(self, x,y,dir=1): self.send(b'G' + p16(x) + p16(y) + p8(dir))
	def absrot_cmd(self, a): self.send(b'A' + p16(a))
	def curve_cmd(self, x,y,alpha,dir=1): self.send(b'Q' + p16(x) + p16(y) + p16(alpha) + p8(dir))
	def turn_cmd(self, o): self.send(b'T' + p16(o))
	def stop_cmd(self): self.send(b'S')
	def setpos_cmd(self, x=0,y=0,o=0): self.send(b'I' + p16(x) + p16(y) + p16(o))
	def intr(self): self.send(b'i')
	def forward_cmd(self, dist): self.send(b'D' + p16(dist))
	def diff_drive_cmd(self, x,y,alpha): self.send(b'L' +  p16(x) + p16(y) + p16(alpha))
	def motor_pwm_cmd(self, m1,m2): self.send(b'm' + p16(m1) + p16(m2))
	def const_speed_cmd(self, m1,m2): self.send(b'M' + p16(m1) + p16(m2))
	def curve_rel_cmd(self, r, alpha): self.send(b'q' +  p16(r) + p16(alpha))
	def speed_cmd(self, s): self.send(b'V' + p8(s))
	#############################
	
	def speed(self, s):
		self.print_cmd('speed',s)
		self.speed_cmd(s)
	
	def forward(self, dist):
		self.print_cmd('forward',dist)
		self.intr()
		self.forward_cmd(dist)
		self.wait_for_arrival()
		
	def move(self, x,y,r=100,dir=1):
		self.print_cmd('moving to', x, y,r,dir)
		self.intr()
		self.point = [x,y]
		self.move_cmd(x,y,r,dir)
		self.wait_for_arrival()
	
	def goto(self, x,y,dir=1):
		self.print_cmd('goto', x, y)
		self.intr()
		self.point = [x,y]
		self.goto_cmd(x,y,dir)
		self.wait_for_arrival()
	
	def absrot(self, a):
		self.print_cmd('absrot', a)
		self.intr()
		self.absrot_cmd(a)
		self.wait_for_arrival()
	
	def curve(self, x,y,alpha,dir=1):
		self.intr()
		self.print_cmd('curve', x,y,alpha,dir)
		self.curve_cmd(x,y,alpha,dir)
		wait_for_arrival()
	
	def curve_rel(self, r, alpha):
		self.intr()
		self.print_cmd('curve_rel', r, alpha)
		self.curve_rel_cmd(r, alpha)
		wait_for_arrival()
	
	def turn(self, o):
		self.print_cmd('turn',o)
		self.intr()
		self.turn_cmd(o)
		self.wait_for_arrival()
	
	def stop(self):
		self.print_cmd('stop')
		self.intr()
		self.stop_cmd()
	
	def setpos(self, x=0,y=0,o=0):
		self.print_cmd('setpos',x,y,o)
		self.setpos_cmd(x,y,o)

	########## [ CONFIG ] #########
	
	def conf_list(self):
		from const_motion import config_bytes,config_ints,config_floats
		confs=config_bytes + config_ints + config_floats
		import textwrap
		print('\n'.join(textwrap.wrap('['+'] ['.join(confs)+']')))

	
	def conf_get_key(self, c):
		from const_motion import config_bytes,config_ints,config_floats
		if c in config_bytes:
			return config_bytes.index(c)
		elif c in config_ints:
			return config_ints.index(c) + len(config_bytes)
		elif c in config_floats:
			return config_floats.index(c) + len(config_bytes) + len(config_ints)
		else: 
			return False

	def conf_float_to_bytes(self, x, decimals=4):
		x *= pow(10, decimals)
		x = int(x)
		s = 1 if x < 0 else 0
		return p32(x) + bytes([s, decimals])
		
	def conf_bytes_to_float(self, x):
		num = l32(x,0)
		s = x[4]
		if s == 1:
			num = -num
		dec = float(x[5])
		return float(num) / pow(10, dec)
	
	
	
	def conf_set(self, k, v, dec=4):
		v = float(v)
		dec = 0 if v == 0 else 9 - ( int(log10(abs(v))) + 1 )
		if not self.use_hash:
			key=self.conf_get_key(k)
			if key == False: return 'Error: key ' + k + ' not found'
		key=p8(key) if not self.use_hash else p16(simple_hash(k))
		to_send=bytearray(self.conf_float_to_bytes(v,dec))
		if self.use_hash: del to_send[-2]
		cmd = b'c' if not self.use_hash else b'h'
		msg = cmd + key + bytes(to_send)
		self.send(msg)
		if self.debug: print(k, ':', self.conf_get(k))
		return True

	def conf_get(self, k):
		if not self.use_hash:
			key=self.conf_get_key(k)
			if not key: return 'Error: key ' + k + ' not found'
		key=p8(key) if not self.use_hash else p16(simple_hash(k))
		cmd = b'C' if not self.use_hash else b'H'
		msg = cmd + key
		self.send(msg)
		while True:
			p = self.read()
			if self.debug: print('conf_get:', chr(p[0]), nice_hex(p[1]))
			if p[0] == b'C'[0]:
				return self.conf_bytes_to_float(p[1])  
		
