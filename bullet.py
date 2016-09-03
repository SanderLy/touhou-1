import pygame
class Bullet(pygame.sprite.Sprite):
	def __init__(self,fname):
		super(Bullet,self).__init__()
		self.fname = fname
		self.image = pygame.image.load('gifs/'+self.fname+'/projectile.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.ctype = ''

	def update(self):
		self.rect.x +=25