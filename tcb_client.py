# Set all the variables necessary to connect to Twitch IRC
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import cfg, socket, time, re, atexit, datetime

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

# network functions go here
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.6', 8888))

while True:
	response = s.recv(1024).decode("utf-8")
	for r in response.split('\r\n'):
		if r.startswith("MOVE"):	#move the arm
			#get the arguments
			args = r.split(' ')
			motor = mh.getMotor(int(args[1]))
			if args[2] == 'FW':
				direction = Adafruit_MotorHAT.FORWARD
			else:
				direction = Adafruit_MotorHAT.BACKWARD
			speed = int(args[3])
			#move the motor
			motor.setSpeed(speed)
			motor.run(direction)
			time.sleep(0.8)
			motor.run(Adafruit_MotorHAT.RELEASE)
