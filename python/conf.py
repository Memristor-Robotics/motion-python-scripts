use_can = 1
# if using multiple motion boards on CAN
motion_can_addr = 600

uart_dev = '/dev/ttyAMA0'
uart_baud=57600
can_dev = 'can0'

use_hash = True

import os
filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf.txt')
if os.path.isfile(filename):
	with open(filename) as f:
		l=f.readline()[:-1]
		if l.lower() == 'uart':
			use_can = 0
		else:
			can_dev = l
else:
	print(filename + ' not exist')

