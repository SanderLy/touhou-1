from character import *

class Marisa(Character):

	def __init__(self, fname, lower, upper, interval, hp, ctype = '', x=0, y=0):
		Character.__init__(self, fname, lower, upper, interval, hp, ctype = '', x=0, y=0)
		self.rect.x = 0
		self.rect.y = 240
		self.ctype = 'character'





