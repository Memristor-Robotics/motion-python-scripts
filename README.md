# Motion python scripts
Short commands for quick control of robot.
Unpack these commands in robot home directory or use by sourcing path.sh.
```bash
cd motion-python-scripts
. path.sh # source path.sh
# control robot
setpos 0 0 0
n 1000
```

Simple command sequences are also supported, look for examples in __tests__ folder.

## Commands

- **repos** - Resets robot position and speed <=> **s R**
- **i** - Send interrupt command (stops currently running command) <=> **s i**
- **p** - (Regulated) Soft Stop (but still keeps position!)
- **P** - Hard Stop
- **moff** - (Motor off) Soft Stop (this will make robot free to move around by hand) <=> **s s**

- **setpos** [x] [y] [o] - Sets robot position
```
x - x coord
y - y coord
o - orientation (in degrees)
```
- **speed** new_speed - Set robot speed
```
new_speed - new robot speed, value in range [0-255]
```


- **n** [d] - Go Straight (forward by default)
```
Go Straight (forward by default)
d - distance in millimeters (negative value to go in other direction) - optional argument
	if this argument is omitted its assumed value of 500
```


- **z** [d] - Go Straight (backward by default)
```
Go Straight (backward by default)
d - distance in millimeters (negative value to go in other direction)
	if this argument is omitted its assumed value of 500
```

- **r** angle - Relative rotate
```
Relative rotate
angle - angle in degrees to rotate
```

- **R** angle - Relative rotate
```
Absolute rotate - rotate robot to point to given angle
angle - angle in degrees to rotate
```

- **G** x y [dir] - Goto (Turn and go) Command
```
x - x coord
y - y coord
radius - radius in which robot can rotate, when robot leaves this circle, it will finish its rotation
dir - {1 - move forward, -1 - move backward, 0 - auto choose}
```

- **N** x y [radius] [dir] - Move (rotate in radius)
```
x - x coord
y - y coord
radius - radius in which robot can rotate, when robot leaves this circle, it will finish its rotation
dir - {1 - move forward, -1 - move backward, 0 - auto choose}
```

- **m** left right - Motor PWM
```
left - left motor pwm (valid value is in range [0-3200])
right - right motor pwm (valid value is in range [0-3200])
```

- **M** left right - Constant Speed
```
Robot constant speed (previous m command was unregulated PWM, this is regulated speed)
left - left wheel speed [0-255]
right - right wheel speed [0-255]
```

- **Q** x y alpha [dir] - Curve
```
rotates around given center (x,y) for alpha angle, in dir direction
x - x coord
y - y coord
alpha - rotation angle around (x,y) center
dir - direction in which robot will go (forward or backward)
```

- **q** radius alpha - Relative Curve
```
Relative curve command - perpendicular center for alpha angle, in dir direction
radius - radius of curve, negative for rotation around on other side
alpha - angle to rotate against perpendicular center, negative to rotate backward
```


- **s** cmd - Send raw command to motion board
```
Send raw command to motion board - it uses UART protocol if UART is used
example:
> s "something"
this sets robot speed to 0x80, you may pass hexadecimal values like \x00, \xff
> s "V\x80"
```




- **d** x y a - Diff drive
```
x - x coord
y - y coord
a - goal angle

for parameters of differential drive there are configuration parameters
conf kp
conf ka
conf kb
If these parameters are wrong, robot might even diverge from goal
```

- **agent** - CAN-TCP router

This command listens for TCP incoming connections (TCP server) and does routing of CAN 
messages to/from TCP clients. So this command is only useful for running GUI and controlling 
robot from it directly without mep2 and possibly drawing some diagrams while robot is running.


- **conf** conf_name [new_value] - Set/Get configuration
```
conf_name - name of configuration to read or set 
new_value - if used, this command will set new value, otherwise it only reads it
--
conf list - to list possible configuration values (currently listed)
```

- **arrows** - control robot with arrow keys
```
Arrows - control robot with arrow keys
this command isn't perfect, maybe it could be made better but it has limitations in OS keyboard processing
because it cannot get key ups, only key downs also delay between 1st and 2nd keystroke is 200ms, which is long
```


- **listen** - listen for commands coming from CAN or UART
- **cancmd** - CAN debugging command (python interactive terminal)

- **bot** - Select CAN device to communicate with or select UART
```bash
bot uart # selected uart
bot can0 # selected can0
bot can1 # selected can1
```

## To control robot inside simulator

run mep2 with some selected robot but don't select any strategy.
- For example:
```bash
ROBOT=helloworld ./main.py
```

This way you can watch robot in blender.


```bash
cd motion-python-scripts
source path.sh
# use bot command to select can device (or robot)
bot can0 # select can0 device
# use commands
n 1000 # move forward 1000 mm
r 150 # rotate 150 deg
```
