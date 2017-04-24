config_bytes = [
	'distance_regulator',
	'rotation_regulator',
	'out_of_control_protection',
	'enable_stuck',
	'stuck',
	'debug',
	'status_change_report',
	'status_send_count',
	'tmr',
	'motor_left_inverted',
	'motor_right_inverted',
	'motor_enable',
	'simulate_encoders',

]
config_ints = [
	'stuck_distance_jump',
	'stuck_rotation_jump',
	'stuck_distance_max_fail_count',
	'stuck_rotation_max_fail_count',
	'motor_speed_limit',
	'motor_rate_of_change',
	'send_status_interval',
	'keep_count',

]
config_floats = [
	'wheel_distance',
	'wheel_r1',
	'wheel_r2',
	'pid_d_p',
	'pid_d_d',
	'pid_r_p',
	'pid_r_d',
	'vmax',
	'omega',
	'accel',
	'alpha',
	'slowdown',
	'slowdown_angle',
	'angle_speedup',
]
