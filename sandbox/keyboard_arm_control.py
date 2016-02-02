from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import cfg, socket, time, re, atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

lr_motor = 			mh.getMotor(4)
shoulder_motor = 	mh.getMotor(3)
elbow_motor = 		mh.getMotor(1)
wrist_motor = 		mh.getMotor(2)

import readchar

print "Press q to quit"
username = ""

while(True):
	c = repr(readchar.readchar()).replace("'", '')
	if c == 'q':
		exit(0)
	elif c == 'a':
		print username, "Left"
		lr_motor.setSpeed(255)
		lr_motor.run(Adafruit_MotorHAT.BACKWARD)
		time.sleep(0.1)
		lr_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 'd':
		print username, 'Right'
		lr_motor.setSpeed(255)
		lr_motor.run(Adafruit_MotorHAT.FORWARD)
		time.sleep(0.1)
		lr_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 'w':
		print username, 'Shoulder Up'
		shoulder_motor.setSpeed(255)
		shoulder_motor.run(Adafruit_MotorHAT.BACKWARD)
		time.sleep(0.1)
		shoulder_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 's':
		print username, 'Shoulder Down'
		shoulder_motor.setSpeed(255)
		shoulder_motor.run(Adafruit_MotorHAT.FORWARD)
		time.sleep(0.1)
		shoulder_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 'u':
		print username, 'Elbow Up'
		elbow_motor.setSpeed(255)
		elbow_motor.run(Adafruit_MotorHAT.FORWARD)
		time.sleep(0.1)
		elbow_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 'j':
		print username, 'Elbow Down'
		elbow_motor.setSpeed(255)
		elbow_motor.run(Adafruit_MotorHAT.BACKWARD)
		time.sleep(0.1)
		elbow_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 'i':
		print username, 'Wrist Up'
		wrist_motor.setSpeed(255)
		wrist_motor.run(Adafruit_MotorHAT.FORWARD)
		time.sleep(0.1)
		wrist_motor.run(Adafruit_MotorHAT.RELEASE)
	elif c == 'k':
		print username, 'Wrist Down'
		wrist_motor.setSpeed(255)
		wrist_motor.run(Adafruit_MotorHAT.BACKWARD)
		time.sleep(0.1)
		wrist_motor.run(Adafruit_MotorHAT.RELEASE)
