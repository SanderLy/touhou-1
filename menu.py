import pygame
import sys
import os
from pygame.locals import *

pygame.init()
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')
mainClock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

	pygame.display.update()
	mainClock.tick(30)