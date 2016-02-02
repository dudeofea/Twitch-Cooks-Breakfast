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

DEVICE = '/dev/video1'
SIZE = (0, 0)				#width / height, set at runtime
CAMERA_SIZE = (640, 480)
FILENAME = 'capture.png'

def camstream():
	#init game, camera, display
	pygame.init()
	pygame.camera.init()
	infoObject = pygame.display.Info()
	SIZE = (infoObject.current_w, infoObject.current_h)
	display = pygame.display.set_mode(SIZE, FULLSCREEN)
	camera = pygame.camera.Camera(DEVICE, CAMERA_SIZE)
	camera.start()
	#camera screen to draw on display
	screen = pygame.surface.Surface(CAMERA_SIZE, 0, display)
	capture = True
	while capture:
		screen = camera.get_image(screen)
		#draw an image on display
		display.blit(screen, (0,0))
		#flip the display buffers thus updating the screen
		pygame.display.flip()
		#handle events
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
				capture = False
			elif event.type == KEYDOWN and event.key == K_s:
				pygame.image.save(screen, FILENAME)
	#die
	camera.stop()
	pygame.quit()
	return

if __name__ == '__main__':
	camstream()
