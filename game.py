import pygame
from pygame.locals import *
import sys
import time
import pyganim

class Character():
    def __init__(self, fname):
        """
        fname is the folder name of the character sprite 
        """
        self.fname = fname


    def animate(self, lower, upper, interval, loop = True):
        """
        lower is the first number of the frame sequence
        upper is the last number of the frame sequence
        interval is the frame delay. all frames will have equal intervals
        """
        self.upper = upper
        self.lower = lower
        self.interval = interval
        self.frames  =[]
        self.loop = loop
        while self.lower <= self.upper:
            dname = 'gifs/' + str(self.fname) + '/' + str(self.lower) + '.png'
            tup = (dname, self.interval) 
            self.frames.append(tup)
            self.lower += 1
        if self.loop:
            return pyganim.PygAnimation(list(self.frames))
        else:
            return pyganim.PygAnimation(list(self.frames), False)


#general variables

#characters initialize
hata = Character('hata')
marisa = Character('marisa')

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Pyganim Test 1')

#hata animations
hata_animation = hata.animate(2, 18, 0.05)

#marisa animations
marisa_idle = marisa.animate(332, 345, 0.05)
marisa_forward_init = marisa.animate(0, 5, 0.05, False)
marisa_forward = marisa.animate(4120, 4127, 0.05)
marisa_backward = marisa.animate(6, 13, 0.05)
marisa_attack = marisa.animate(14,34, 0.05, False)
marisa_animation = marisa_idle

#idle animations start
hata_animation.play() # there is also a pause() and stop() method
marisa_animation.play() # there is also a pause() and stop() method

#default positions set for hata
x = 0
y = 0
#default positions set for marisa
x2 = 0
y2 = 0

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
                # press "L" key to stop looping
                marisa_animation.pause()
                marisa_animation = marisa_idle
                marisa_animation.play()
                #hata_animation.loop = False
                #marisa_animation.loop = False
                #x +=10
                #print ('l is pressed')
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
        if x2>0:
            marisa_animation = marisa_backward
            marisa_animation.play()
            x2-=10
    if keys[pygame.K_RIGHT]:
        if x2<914:            
            marisa_animation = marisa_forward
            marisa_animation.play()
            x2+=10            
    if keys[pygame.K_UP]:
        if y2 > 0:
            y2-=10
    if keys[pygame.K_DOWN]:
        if y2 < 524:
            y2+=10
    if keys[pygame.K_z]:
        marisa_animation = marisa_attack
        marisa_animation.play()

    hata_animation.blit(windowSurface, (x, y))
    marisa_animation.blit(windowSurface, (x2, y2))

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.