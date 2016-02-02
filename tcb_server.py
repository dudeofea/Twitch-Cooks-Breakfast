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

PINK1			= (255,	158,174)
RED1			= (219,	80,	74)
RED2			= (183,	63,	92)
DARK			= (34,	29,	35)
LIGHT			= (252,	247,255)

DEVICE = '/dev/video1'
SIZE = (1500, 1000)				#width / height, set at runtime
CAMERA_SIZE = (640, 480)
FILENAME = 'capture.png'

class ChatSurface(pygame.Surface):
	def __init__(self, size_wh, header_font):
		pygame.Surface.__init__(self, size_wh)
		self.size_wh = size_wh
		self.header_font = header_font
	def draw(self, screen):
		self.fill(LIGHT)
		header_label 			= self.header_font.render("Twitch Cooks Breakfast", 1, LIGHT)
		header_label_shadow 	= self.header_font.render("Twitch Cooks Breakfast", 1, RED1)
		pygame.draw.rect(self, PINK1, [0, 0, self.size_wh[0], 70])				#header background
		header_pad = (self.size_wh[0] - header_label.get_width()) / 2
		self.blit(header_label_shadow, (2 + header_pad, 12))
		self.blit(header_label, (header_pad, 10))
		screen.blit(self, (SIZE[0] - self.size_wh[0], 0))

def main():
	#init game, camera, display
	pygame.init()
	leckerli_font = pygame.font.Font("fonts/LeckerliOne-Regular.ttf", 35)
	pygame.camera.init()
	infoObject = pygame.display.Info()
	#SIZE = (infoObject.current_w, infoObject.current_h)
	screen = pygame.display.set_mode(SIZE, 0)#FULLsurface)
	camera = pygame.camera.Camera(DEVICE, CAMERA_SIZE)
	camera.start()
	#initialize surfaces
	camera_surface = pygame.surface.Surface(CAMERA_SIZE, 0, screen)
	chat_surface = ChatSurface((400, SIZE[1]), leckerli_font)
	capture = True
	while capture:
		#get camera image
		camera_surface = camera.get_image(camera_surface)
		#draw the screen elements
		pygame.draw.rect(screen, DARK, [0, 0, SIZE[0], SIZE[1]])				#background color
		screen.blit(camera_surface, (0,0))										#camera screen
		chat_surface.draw(screen)
		#flip the display buffers thus updating the surface
		pygame.display.flip()
		#handle events
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
				capture = False
			elif event.type == KEYDOWN and event.key == K_s:
				pygame.image.save(surface, FILENAME)
	#die
	camera.stop()
	pygame.quit()

if __name__ == '__main__':
	main()
