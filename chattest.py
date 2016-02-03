# Set all the variables necessary to connect to Twitch IRC
#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import cfg, socket, time, re, atexit, datetime

# create a default object, no changes to I2C address or frequency
# mh = Adafruit_MotorHAT(addr=0x60)
# # recommended for auto-disabling motors on shutdown!
# def turnOffMotors():
# 	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
# 	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
# 	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
# 	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
# atexit.register(turnOffMotors)
#
# lr_motor = 			mh.getMotor(4)
# shoulder_motor = 	mh.getMotor(3)
# elbow_motor = 		mh.getMotor(1)
# wrist_motor = 		mh.getMotor(2)

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

done_wait = datetime.datetime.now()
rot_time = 0.8
wait_time = 12

while True:
	response = s.recv(1024).decode("utf-8")
	for r in response.split('\r\n'):
		if datetime.datetime.now() < done_wait:
			continue
		if r == "PING :tmi.twitch.tv\r\n":
		    s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		    print("Pong")
		elif len(r) > 0:
			username = re.search(r"\w+", r).group(0) # return the entire match
			message = CHAT_MSG.sub("", r)
			#print(username + ": " + message)
			if message.lower() in ['l', 'left']:		#left
				print username, "Left"
				lr_motor.setSpeed(255)
				lr_motor.run(Adafruit_MotorHAT.BACKWARD)
				time.sleep(rot_time)
				lr_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['r', 'right']:
				print username, 'Right'
				lr_motor.setSpeed(255)
				lr_motor.run(Adafruit_MotorHAT.FORWARD)
				time.sleep(rot_time)
				lr_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['su', 'shoulder up']:
				print username, 'Shoulder Up'
				shoulder_motor.setSpeed(255)
				shoulder_motor.run(Adafruit_MotorHAT.BACKWARD)
				time.sleep(rot_time)
				shoulder_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['sd', 'shoulder down']:
				print username, 'Shoulder Down'
				shoulder_motor.setSpeed(255)
				shoulder_motor.run(Adafruit_MotorHAT.FORWARD)
				time.sleep(rot_time)
				shoulder_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['eu', 'elbow up']:
				print username, 'Elbow Up'
				elbow_motor.setSpeed(255)
				elbow_motor.run(Adafruit_MotorHAT.FORWARD)
				time.sleep(rot_time)
				elbow_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['ed', 'elbow down']:
				print username, 'Elbow Down'
				elbow_motor.setSpeed(255)
				elbow_motor.run(Adafruit_MotorHAT.BACKWARD)
				time.sleep(rot_time)
				elbow_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['wu', 'wrist up']:
				print username, 'Wrist Up'
				wrist_motor.setSpeed(255)
				wrist_motor.run(Adafruit_MotorHAT.FORWARD)
				time.sleep(rot_time)
				wrist_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
			elif message.lower() in ['wd', 'wrist down']:
				print username, 'Wrist Down'
				wrist_motor.setSpeed(255)
				wrist_motor.run(Adafruit_MotorHAT.BACKWARD)
				time.sleep(rot_time)
				wrist_motor.run(Adafruit_MotorHAT.RELEASE)
				done_wait = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
