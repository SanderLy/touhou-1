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
        self.x = 0
        self.y = 0


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
        self.y-=10
    def move_down(self):
        self.y+=10
    def move_left(self):
        self.x-=10
    def move_right(self):
        self.x+=10