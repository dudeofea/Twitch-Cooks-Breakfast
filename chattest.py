# Set all the variables necessary to connect to Twitch IRC
import cfg
import socket
import time
import re

def chat(sock, msg):
	sock.send("PRIVMSG #{} :{}".format(cfg.CHAN, msg))

def ban(sock, user):
	chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=60):
	chat(sock, ".timeout {}".format(user, secs))

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

while True:
	response = s.recv(1024).decode("utf-8")
	for r in response.split('\r\n'):
		if r == "PING :tmi.twitch.tv\r\n":
		    s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		    print("Pong")
		elif len(r) > 0:
			username = re.search(r"\w+", r).group(0) # return the entire match
			message = CHAT_MSG.sub("", r)
			#print(username + ": " + message)
			if message == 'l':		#left
				print username, "Left"
			elif message == 'r':
				print username, 'Right'
		    #print "Unknown:", r
