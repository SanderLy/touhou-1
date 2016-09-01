import pygame
from pygame.locals import *
import sys
import time
import pyganim
from marisa import *

hata = Character('hata')
marisa = Marisa('marisa')

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')

hata_animation = hata.animate(2, 18, 0.05)
marisa_idle = marisa.animate(332, 345, 0.05)
marisa_forward_init = marisa.animate(0, 5, 0.05)
marisa_forward = marisa.animate(4120, 4127, 0.05)
marisa_animation = marisa_idle

hata_animation.play() # there is also a pause() and stop() method
marisa_animation.play() # there is also a pause() and stop() method
x = 0
y = 0

mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)
while True:
    windowSurface.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                marisa_animation.pause()
                marisa_animation = marisa_idle
                marisa_animation.play()
    keys = pygame.key.get_pressed()  #checking pressed keys
    """    
    x-axis left boundary, y-axis top boundary = 0
    x-axis right boundary = frame width - model width - 10
    y-axis bottom boundary = frame height - model height
    """
    if keys[pygame.K_d]:
        if x<931:
            x += 10
    if keys[pygame.K_a]:
        if x > 0:
            x-=10
    if keys[pygame.K_w]:
        if y > 0:
            y-=10
    if keys[pygame.K_s]:
        if y < 430:
            y+=10
    if keys[pygame.K_LEFT]:
        if marisa.x>0:
            marisa_animation = marisa_forward
            marisa_animation.play()
            marisa.move_left()
    if keys[pygame.K_RIGHT]:
        if marisa.x<914:
            marisa_animation = marisa_forward
            marisa_animation.play()
            marisa.move_right()         
    if keys[pygame.K_UP]:
        if marisa.y > 0:
            marisa.move_up()
    if keys[pygame.K_DOWN]:
        if marisa.y < 524:
            marisa.move_down()
            #60 is da magic numbah
    hata_animation.blit(windowSurface, (x, y))
    marisa_animation.blit(windowSurface, (marisa.x, marisa.y))

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.