#!/usr/bin/python

import sys
sys.path.append('/home/pi/python')
from engine import *

import time

motor(200, 200)
time.sleep(10)
intr()

