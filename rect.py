import pygame
import sys
import time
import pyganim
import os
import random
from pygame.locals import *
from marisa import *
from mamizou import *
from bullet import *
from mob import *

windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')
mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)


while True:
	windowSurface.fill(BGCOLOR)
	now = pygame.time.get_ticks()

	
	
	
	
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

	
	

	sprites_list.draw(windowSurface)
	pygame.display.flip()
	pygame.display.update()
	mainClock.tick(30)