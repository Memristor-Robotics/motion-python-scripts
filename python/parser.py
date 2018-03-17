import sys
sys.path.append('/home/pi/python')
from convert import l16

def P_cmd(p):
	# print(len(p), p)
	print(p[0] + " (" + str(l16(p, 1)) + ", " + str(l16(p, 3)) + ")  angle: " + str(l16(p, 5))) 

def do_nothing(p):
	pass

packets = {
	'P': P_cmd,
	'p': P_cmd,
	'F': do_nothing,
	'A': do_nothing
}

