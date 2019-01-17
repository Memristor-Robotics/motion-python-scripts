
servo_id = 0x00008D70
c=[]
def klapna(v):
	global c
	c.servo(3, 'GoalPosition', 95 if v == 1 else 225, servo_id)
	c.servo(3, 'Speed', 1000, servo_id)
def cev2(v):
	global c
	c.servo(20, 'GoalPosition', 130 if v == 0 else 200, servo_id)
def cev(v):
	global c
	c.servo(5, 'GoalPosition', 805 if v == 0 else 703, servo_id)

def prekidac(v):
	global c
	c.servo(1, 'GoalPosition', 272 if v == 0 else 0, servo_id)
def pcelica(v):
	global c
	c.servo(7, 'GoalPosition', 815 if v == 1 else (600 if v == 2 else 221), servo_id)
def load_cfg(r):
	global c
	c = r
	r.conf_set('send_status_interval', 100)
	r.conf_set('enable_stuck', 1)
	r.conf_set('wheel_r1', 68.0)
	r.conf_set('wheel_r2', 67.25513)
	r.conf_set('wheel_distance', 252.30)

	setpid = False
	if setpid:
		r.conf_set('pid_d_p', 2.75)
		r.conf_set('pid_d_d', 60)
		r.conf_set('pid_r_p', 2.2)
		r.conf_set('pid_r_d', 100)
		r.conf_set('pid_r_i', 0.033)
	r.conf_set('accel', 700)
