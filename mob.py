from character import *

class Mob(Character):

	def __init__(self, fname, lower, upper, interval, hp, mtype = '', x=0, y=0):
		Character.__init__(self, fname, lower, upper, interval, hp, ctype = '', x=0, y=0)
		self.ctype = 'mob'
		self.rect.x = pygame.mouse.get_pos()[0]
		self.rect.y = pygame.mouse.get_pos()[1]
		self.last_fire = 0
		# self.rect.x = 80
		# self.rect.y = 199