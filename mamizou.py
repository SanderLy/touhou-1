from character import *

class Mamizou(Character):

	def __init__(self, fname, lower, upper, interval, hp, ctype = '', x=0, y=0):
		Character.__init__(self, fname, lower, upper, interval, hp, ctype = '', x=0, y=0)
		self.ctype = 'character'
		self.rect.x = 920
		self.rect.y = 80
		