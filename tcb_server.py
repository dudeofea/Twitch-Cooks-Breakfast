#!/usr/bin/python
#
#	Server / Game Display for Twitch Cooks Breakfast
#
#	Talks to the pi running tcb_client.py, and runs
#	the logic and game overlay on top of the camera
#	feed. Sends movement commands to the pi.
#
import pygame
import pygame.camera
from pygame.locals import *
import cfg, socket, time, re, atexit, datetime
from threading import Thread

PINK1			= (255,	158,174)
RED1			= (219,	80,	74)
RED2			= (183,	63,	92)
DARK			= (34,	29,	35)
LIGHT			= (252,	247,255)

DEVICE = '/dev/video0'
SIZE = (1500, 1000)				#width / height, set at runtime
CAMERA_SIZE = (800, 600)
FILENAME = 'capture.png'

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

class ChatSurface(pygame.Surface):
	def __init__(self, size_wh, header_font, text_font, text_font_bold):
		pygame.Surface.__init__(self, size_wh)
		self.size_wh = size_wh
		self.header_font 	= header_font
		self.text_font 		= text_font
		self.text_font_bold = text_font_bold
		self.text_height 	= self.text_font.render("some sentence", 1, LIGHT).get_height()
		self.max_lines 		= int((self.size_wh[1] - 100) / (self.text_height+2))
		self.lines = []
		self.running = True
		self.chat_thread 	= Thread(target = self.read_chat)
		self.chat_thread.start()
	def add_line(self, user, comment, color=DARK):
		#add to front of list
		self.lines.insert(0, (user, comment, color))
		#clip list when neccesary
		if len(self.lines) > self.max_lines:
			self.lines = self.lines[:self.max_lines]
	def read_chat(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((cfg.HOST, cfg.PORT))
		s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
		s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
		s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))
		while self.running:
			response = s.recv(1024).decode("utf-8")
			print response
			for r in response.split('\r\n'):
				if r == "PING :tmi.twitch.tv\r\n":
				    s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
				elif len(r) > 0 and CHAT_MSG.match(r):
					username = re.search(r"\w+", r).group(0) # return the entire match
					message = CHAT_MSG.sub("", r)
					self.add_line(username, message)
					#print(username + ": " + message)
	def draw(self, screen):
		#draw white background
		self.fill(LIGHT)
		#draw comments
		for x in xrange(0, len(self.lines)):
			l = self.lines[x]
			user_label = self.text_font_bold.render(l[0]+": ", 1, RED1)
			self.blit(user_label, (15, self.size_wh[1] - x * (self.text_height+2) - 30))
			self.blit(self.text_font.render(l[1], 1, l[2]), (10 + user_label.get_width(), self.size_wh[1] - x * (self.text_height+2) - 30))
		#draw header
		header_label 			= self.header_font.render("Twitch Cooks Breakfast", 1, LIGHT)
		header_label_shadow 	= self.header_font.render("Twitch Cooks Breakfast", 1, RED1)
		pygame.draw.rect(self, PINK1, [0, 0, self.size_wh[0], 70])				#header background
		header_pad = (self.size_wh[0] - header_label.get_width()) / 2
		self.blit(header_label_shadow, (2 + header_pad, 12))
		self.blit(header_label, (header_pad, 10))
		#draw on screen
		screen.blit(self, (SIZE[0] - self.size_wh[0], 0))
	def stop(self):
		self.running = False

def main():
	#init game, camera, display
	pygame.init()
	leckerli_font = pygame.font.Font("fonts/LeckerliOne-Regular.ttf", 35)
	anon_font	  = pygame.font.Font('fonts/slkscr.ttf', 15)
	anon_font_bold= pygame.font.Font('fonts/slkscrb.ttf', 15)
	pygame.camera.init()
	infoObject = pygame.display.Info()
	#SIZE = (infoObject.current_w, infoObject.current_h)
	screen = pygame.display.set_mode(SIZE, 0)#FULLsurface)
	camera = pygame.camera.Camera(DEVICE, CAMERA_SIZE)
	camera.start()
	#initialize surfaces
	camera_surface = pygame.surface.Surface(CAMERA_SIZE, 0, screen)
	chat_surface = ChatSurface((400, SIZE[1]), leckerli_font, anon_font, anon_font_bold)
	chat_surface.add_line("Some Guy", "Hey buttmunch")
	chat_surface.add_line("anon353424", "wuuutttttttttttt")
	print chat_surface.lines
	capture = True
	while capture:
		#get camera image
		camera_surface = camera.get_image(camera_surface)
		#draw the screen elements
		pygame.draw.rect(screen, DARK, [0, 0, SIZE[0], SIZE[1]])				#background color
		screen.blit(pygame.transform.scale(camera_surface, SIZE), (0,0))										#camera screen
		chat_surface.draw(screen)
		#flip the display buffers thus updating the surface
		pygame.display.flip()
		#handle events
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
				capture = False
			elif event.type == KEYDOWN and event.key == K_s:
				pygame.image.save(camera_surface, FILENAME)
	#die
	chat_surface.stop()
	camera.stop()
	pygame.quit()

if __name__ == '__main__':
	main()
