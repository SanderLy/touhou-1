import pygame
from pygame.locals import *
import sys
import time
import pyganim

class Character(pygame.sprite.Sprite):
    def __init__(self, fname, lower, upper, interval, hp, ctype ='', x = 0, y = 0):
        """
        fname is the folder name of the character sprite
        ctype for type of character 
        """
        self.fname = fname
        self.hp = hp
        self.ctype = ctype
        super(Character,self).__init__()
        
        #frames for death frame
        self.dframes = [('gifs/' + str(self.fname) + '/' + 'hitbox' + '.png', 0.05)]    
        self.animation = pyganim.PygAnimation(list(self.dframes))
        self.animation.loop = False
        self.animation.play()

        #frames for alive(idle) animation
        self.upper = upper
        self.lower = lower
        self.interval = interval
        self.frames  =[]
        while self.lower <= self.upper:
            dname = 'gifs/' + str(self.fname) + '/' + str(self.lower) + '.png'
            tup = (dname, self.interval) 
            self.frames.append(tup)
            self.lower += 1
        self.animation2 = pyganim.PygAnimation(list(self.frames))
        self.animation2.play()
        self.setHitbox(x,y)

    def setHitbox(self,x,y):
        #static image for hitbox
        self.image = pygame.image.load('gifs/' + str(self.fname) + '/' + 'hitbox' + '.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
    def animate(self, lower, upper, interval):
        """
        lower is the first number of the frame sequence
        upper is the last number of the frame sequence
        interval is the frame delay. all frames will have equal intervals
        """
        self.upper = upper
        self.lower = lower
        self.interval = interval
        self.frames  =[]
        while self.lower <= self.upper:
            dname = 'gifs/' + str(self.fname) + '/' + str(self.lower) + '.png'
            tup = (dname, self.interval) 
            self.frames.append(tup)
            self.lower += 1
        return pyganim.PygAnimation(list(self.frames))       

    def move_up(self):
        self.rect.y-=10
    def move_down(self):
        self.rect.y+=10
    def move_left(self):
        self.rect.x-=10
    def move_right(self):
        self.rect.x+=10