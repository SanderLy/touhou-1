import pygame
class Bullet(pygame.sprite.Sprite):
	def __init__(self,fname,btype):
		super(Bullet,self).__init__()
		self.fname = fname
		self.image = pygame.image.load('gifs/'+self.fname+'/projectile.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.btype = btype

	def update(self):
		if self.btype == 'character':
			self.rect.x +=25
		if self.btype == 'mob':
			self.rect.x -= 25
