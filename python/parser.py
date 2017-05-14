import io



f = io.open("/dev/serial0", "rb")

K1_deg = 0.0062428419502617806
table = {0: ("speed",1), 
         1: ("angle_diff",1), 
         2: ("rot_speed",K1_deg),
         3: ("dist",1),
         4: ("orientation", K1_deg),
         5: ("goal_angle", K1_deg),
         6: ("x", 1),
         7: ("y", 1),
         8: ("atan2", 1),
         25: ("X",1),
         26: ("Y",1),
         0xff: ("starting N",1)}
while True:
    code = ord(f.read(1))
    if code == ord('\r'):
        print("\n\n")
    else:
        if code in table:
            a = ord(f.read(1))
            b = ord(f.read(1))
            n = ((a << 8) | b)
            if n > 2**15:
                n = -(2**16 - n)

            print(table[code][0] + ": " + str(n * table[code][1]))

