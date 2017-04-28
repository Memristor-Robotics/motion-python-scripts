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
ack = True 
def settol(t):
    global tol
    tol = t
def wait_for_ack(cmd):
    if not ack: return True
    timeout = 20
    while ack and timeout > 0:
        if chdata():
            pkt = read()
            if chr(pkt[0]) == 'A' and pkt[1] == cmd:
                return True
        else:
            time.sleep(0.01)
    return False
def wait_for_arrival():
    global tol
    while True:
        pkt = read()
        p = pkt[1]
        if chr(pkt[0]) == 'p':
            #print("pkt p: ", pkt[1])
            print("p")
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
def send_ack(m):
    while True:
        send(m)
        if wait_for_ack(m[0]): break
def move_to_cmd(x,y,r=100,o=1):
    send_ack("N" + pack(x) + pack(y) + chr(to_uchar(o)) + pack(r))
def goto_cmd(x,y,r=100,o=1):
    send_ack("G" + pack(x) + pack(y) + chr(to_uchar(o)))
def turn_cmd(o):
    send_ack("T" + pack(o))
def speed(s):
    send_ack('V' + chr(s))
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

def motor(a,b):
    send(commands['motor'] + pack(a) + pack(b))

def turn(o):
    print('turn: ', o)
    intr()
    turn_cmd(o)
    wait_for_arrival()
def setpos(x,y,o=0):
    send_ack('I' + pack(x) + pack(y) + pack(o))

