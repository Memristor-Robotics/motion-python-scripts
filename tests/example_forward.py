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

r.tol = 0
from config import *
load_cfg(r)
##
r.setpos(0,0)
r.speed(150)
##


#######################
# TASK
#######################

r.goto(300,0)
r.goto(-300,0)
