import pygame
import sys
import os
from pygame.locals import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50) # set initial screen position

pygame.init()
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')
menu  = pygame.image.load('UI/how_to_play.png').convert_alpha()
mainClock = pygame.time.Clock()
pygame.mixer.music.load('sfx/bgm1.ogg')
pygame.mixer.music.play(-1,0.0)
menu_accept = pygame.mixer.Sound('sfx/menu_decline.wav')

while 1:
	windowSurface.blit(menu,(0,0))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			menu_accept.play()
			pygame.mixer.music.fadeout(1000)
			execfile('menu.py')
			sys.exit()				
	mainClock.tick(30)