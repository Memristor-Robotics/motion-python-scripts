#!/usr/bin/python3

import sys, os, time
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
#  async_result = pool.apply_async(foo, ('world', 'foo')) # tuple of args for foo
sys.path.append(os.environ['PYTHON'])
from Engine import *
from com.Can import Can
r=Engine()

#pool.apply_async(lambda: (time.sleep(0.7), r.t(0)) )
######################

from config import *
load_cfg(r)
##
r.tol = 0
r.setpos(0,0)
r.speed(50)
##

from math import *
r.conf_set('send_status_interval', 100)
r.setpos(0,0)
r.speed(50)
r.conf_set('accel', 900)
r.conf_set('alpha', 1000)

r.tol = 0
d=-1000
for i in range(2):
	r.move(300, 200, 400)
	r.move(0,-200, 400)
	time.sleep(0.2)
	r.forward(-d)
	time.sleep(0.2)
	r.forward(d)

