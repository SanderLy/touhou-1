import pygame
import sys
import os
from pygame.locals import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50) # set initial screen position

pygame.init()
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')
menu  = pygame.image.load('UI/title_screen_bg.png').convert_alpha()
menu_cursor = pygame.image.load('UI/button_hover.png').convert_alpha()
menu_cursor_index = 0
menu_flag = True
menu_flag2 = False
menu_cursor_y = 300
mainClock = pygame.time.Clock()
pygame.mixer.music.load('sfx/bgm1.ogg')
pygame.mixer.music.play(-1,0.0)
menu_select = pygame.mixer.Sound('sfx/menu_select.wav')
menu_accept = pygame.mixer.Sound('sfx/menu_accept.wav')

while menu_flag:

	windowSurface.blit(menu,(0,0))
	windowSurface.blit(menu_cursor,(0,menu_cursor_y))

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			menu_select.stop()
			if event.key == K_DOWN:
				menu_select.stop()
				menu_select.play()
				if menu_cursor_y <= 400:
					menu_cursor_y += 100
					menu_cursor_index +=1
				else:
					menu_cursor_y = 300
					menu_cursor_index = 0
			if event.key == K_UP:
				menu_select.stop()
				menu_select.play()
				if menu_cursor_y > 300:
					menu_cursor_y -= 100
					menu_cursor_index-=1
				else:
					menu_cursor_y = 500
					menu_cursor_index = 2
			if event.key == K_RETURN:
				menu_accept.play()
				if menu_cursor_index == 0:
					pygame.mixer.music.fadeout(1000)
					execfile('game.py')
					sys.exit()
				elif menu_cursor_index == 1:
					pygame.mixer.music.fadeout(1000)
					execfile('htp.py')
					sys.exit()
				elif menu_cursor_index == 2:
					pygame.mixer.music.fadeout(1000)
					pygame.quit()
					sys.exit()
	pygame.display.update()
	mainClock.tick(30)