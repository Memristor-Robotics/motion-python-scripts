
servo_commands = {
	'ModelNumber': [0, 'R', 'h'],

	'SetId': [3, 'RW', 'B'],
	'SetBaud': [4, 'RW', 'B'],
	'ReturnDelayTime': [5, 'RW', 'B'],
	'CWAngleLimit': [6, 'RW', 'h'],
	'CCWAngleLimit': [8, 'RW', 'h'],
	'HLimitTemp': [11, 'RW', 'B'],
	'MinVoltage': [12, 'RW', 'B'],
	'MaxVoltage': [13, 'RW', 'B'],
	'MaxTorque': [14, 'RW', 'h'],
	'Status': [16, 'RW', 'B'],
	'AlarmLED': [17, 'RW', 'B'],
	'AlarmShutdown': [18, 'RW', 'B'],
	'TorqueEnable': [24, 'RW', 'B'],
	'LED': [25, 'RW', 'B'],
	'CWComplianceMargin': [26, 'RW', 'B'],
	'CCWComplianceMargin': [27, 'RW', 'B'],
	'CWComplianceScope': [28, 'RW', 'B'],
	'CCWComplianceScope': [29, 'RW', 'B'],
	'GoalPosition': [30, 'RW', 'h'],
	'Speed': [32, 'RW', 'h'],
	'TorqueLimit': [34, 'RW', 'B'],
	'PresentPosition': [36, 'R', 'h'],
	'PresentSpeed': [38, 'R', 'h'],
	'PresentLoad': [40, 'R', 'h'],
	'PresentVoltage': [42, 'R', 'B'],
	'PresentTemp': [43, 'R', 'B'],
	'Punch': [48, 'RW', 'h'],
}

robot_servos = {
	'ColorServo': ['ax', 7],
	'Stopper': ['ax', 6],
	'TrackLeft': ['ax', 4],
	'TrackRight': ['ax', 9],
	'HandLeft': ['ax', 2],
	'HandRight': ['ax', 11],
	'Pump': ['ax', 5],
	'Limiter': ['ax', 6],
	'SDir': ['ax', 20],
	'SSide': ['ax', 21],
    'SBall': ['ax', 50]
}

robot_byte_act = {
	'CircularEjector': [0x7f05, 'W'],
	'Rope': [0x7f09, 'R'],
	'Pump': [0x7f02, 'W'],
	'Cylinder': [0x7f03, 'W'],
	'Color': [0xab01, 'W'],
	'FunnyAction': [0xab02, 'W'],
	'BigTrack': [0x7f06, 'W'],
	'BackInfra': [0x7f10, 'R'],
	'FrontInfra': [0x7f0e, 'R'],
	'MiddleInfra': [0x7f0d, 'R'],
	'ColorRotator': [0x7f12, 'W'],
	'ColorRotator2': [0x7f07, 'W'],
	'SColorRotator1': [0x7f13, 'W'],
	'SColorRotator2': [0x7f14, 'W'],
	
}


def listServoCmds():
	print('Servo commands:')
	for i in sorted(servo_commands):
		print('\t' + i)

def listServo():
	print('Servo list:')
	for i in sorted(robot_servos):
		print('\t' + i)

def listActuators():
	print('Actuators, Sensors:')
	for i in sorted(robot_byte_act):
		print('\t' + i)
