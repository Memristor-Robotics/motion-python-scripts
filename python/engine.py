from math import sqrt
from read import *
from send import *
from convert import *
from conf import *
from parser2 import *
status_idle = 'I'
def vec_length(x,y):
    return sqrt(x**2+y**2)

debug = 0
point = [1,2]
tol = 40
def wait_for_arrival():
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
def move_to_cmd(x,y,r=100,o=1):
    send("N" + pack(x) + pack(y) + chr(to_uchar(o)) + pack(r))
def goto_cmd(x,y,r=100,o=1):
    send("G" + pack(x) + pack(y) + chr(to_uchar(o)))
def turn_cmd(o):
    send("T" + pack(o))
def speed(s):
    send('V' + chr(s))
def intr():
    send('i')
def move(x,y,r=100,o=1):
    print('moving to: ', x, y)
    intr()
    point = [x,y]
    move_to_cmd(x,y,r,o)
    wait_for_arrival()

def goto(x,y,o=1):
    print('goto: ', x, y)
    intr()
    point = [x,y]
    goto_cmd(x,y,o)
    wait_for_arrival()

def turn(o):
    print('turn: ', o)
    intr()
    turn_cmd(o)
    wait_for_arrival(0)
def setpos(x,y,o=0):
    send('I' + pack(x) + pack(y) + pack(o))

