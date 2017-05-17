import socket
import struct
import sys
import binascii
import time
from conf_can import *

class mycan:

    def __init__(self, addr=0, debug=0):
        self.addr = addr
        self.can_frame_fmt = "=IB3x8s"
        self.use_eff = 0x80000000
        self.debug = debug
        self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        iface = 'can0'
        self.s.bind((iface,))

    def _build_can_frame(self, can_id, data):
               can_dlc = len(data)
               data = data.ljust(8, b'\x00')
               return struct.pack(self.can_frame_fmt, can_id | self.use_eff, can_dlc, data)

    def _dissect_can_frame(self,frame):
               can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, frame)
               return (can_id, can_dlc, data[:can_dlc], binascii.hexlify(data[:can_dlc]))


    def swap32(i):
            return struct.unpack("<I", struct.pack(">I", i))[0]

    def set_addr(self, a):
        self.addr = a

    def nice_hex(s, spaces=4):
        h = binascii.hexlify(s).decode('ascii')
        return ' '.join([h[i:i+spaces] for i in range(0, len(h)-(len(h)%spaces)+spaces, spaces)])

    def raw(self,_addr,f,val):
        ''' f, val '''
        frame = self._build_can_frame(_addr, struct.pack(f, *val))
        if self.debug:
            print('[debug] sent: ' + mycan.nice_hex(frame))
        self.s.send(frame)

    def graw(self,id=None):
        while True:
            frame = self._dissect_can_frame(self.s.recv(16))
            if id == None or id == frame[0]:
                print(hex(frame[0]) + ": " + mycan.nice_hex(frame[2]))
                break

    def servo(self,which,f,val=None):
        if which not in robot_servos:
            print('servo ' + which + ' doesn\'t exist')
            return

        if f not in servo_commands:        
            print('function ' + f + ' doesn\'t exist')
            return

        servo = robot_servos[which]
        cmd = servo_commands[f]
        servo_id = servo[1]
        servo_len = 4
        servo_func = cmd[0]
        servo_rw = cmd[1]
        servo_fmt = cmd[2]

        if val == None and 'R' not in servo_rw:
            print('function ' + f + ' is not readable')
            return

        if val != None and 'W' not in servo_rw:
            print('function ' + f + ' is not writable')
            return

        if val == None:
            servo_rw = 2
            servo_fmt = ''
        else:
            servo_rw = 3

        if val == None:
            servo_len = 3
        elif servo_fmt == 'h':
            servo_len += 1


        

        addr = 0x7f00 if servo[0] == 'ax' else 0x7f01
        fmt = '4B'+servo_fmt
        data = [servo_id, servo_len, servo_rw, servo_func]
        if val != None:
            data += [val]

        self.raw(addr, fmt, data)
        if val == None:
            print('Sent request, waiting for answer')
            while True:
                frame = self._dissect_can_frame(self.s.recv(16))
                if frame[0] == addr and frame[1] > 0 and frame[2][0] == servo_id:
                    dlc = frame[1]
                    servo_len = frame[2][3]-3
                    servo_fmt = 'B'
                    if servo_len == 2:
                        servo_fmt = 'h'
                    print(which + ': ' + struct.unpack(servo_fmt, frame[2][len(frame[2])-(servo_len+1):dlc-1]))
                    return


    def actuator(self, which, val=None):
        '''
            which - which actuator to send data to
            val - value to write
                  (omitt if reading sensor)
        '''
        if which not in robot_byte_act:
            print('sensor or actuator ' + which + ' doesn\'t exist')
            return

        act = robot_byte_act[which]

        if val != None and 'W' not in act[1]:
            print('Cannot write to sensor')
        
        if val == None and 'R' not in act[1]:
            print('Cannot read from actuator')

        data = []
        if val != None:
            data = [val]
        else:
            print("reading from sensor not implemented yet")

        c.raw(act[0], 'B', [val])
        

            
c=mycan()
