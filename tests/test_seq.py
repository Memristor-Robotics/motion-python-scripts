#!/usr/bin/python
import sys
sys.path.append('/home/pi/python')
from engine import *

conf_set('send_status_interval', 200)
setpos(610,-790,-90)
tol=0
speed(70)
move(360,-550,180,-1)

# task raketa
goto(360, -720, -1)
goto(360, -750, 1)
goto(360, -720, -1)
goto(360, -750, 1)
goto(360, -720, -1)

# sanzer
tol=40
move(350,-750,100,-1)
tol=150
move(25, -200,150,-1)
tol=0
move(25,30,30,-1)
