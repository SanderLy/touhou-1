import pygame
import sys
import time
import pyganim
import os
from pygame.locals import *
from marisa import *
from mamizou import *
from bullet import *
from mob import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50) # set initial screen position


pygame.init()

#set up the window
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')

#create the list of sprites
projectile_list =  pygame.sprite.Group()
sprites_list = pygame.sprite.Group()
collide_list = pygame.sprite.Group()

#instantiate the sprites
hp = pygame.image.load('hp_bar/marisa_health.png').convert_alpha()
mp = pygame.image.load('hp_bar/mp.png').convert_alpha()
marisa = Marisa('marisa',332,345,0.05, 10,'character')
mamizou = Mamizou('mamizou',1,15,0.09,10,'character')

#add each sprite inside the list of sprites for hitbox checking
sprites_list.add(marisa)
sprites_list.add(mamizou)

marisa_idle = marisa.animate(332, 345, 0.05)
marisa_forward = marisa.animate(4120, 4127, 0.05)
marisa_animation = marisa_idle


# Projectile Animation for marisa

press_event  = 0
now = 0
rate = 300
#---------------------------------

#mob respawn rate 

click_event = 0
mob_rate = 300

resource = 5000

#---------------------------------

#mob indices
type_mob = {1:(0,1),2:(2,3),3:(4,5)}
current_mob = 1


#printing of label
font = pygame.font.Font(None, 35)

marisa_animation.play()
mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)
cooldown = 1

#---------------------------------

#try animationn of mp bar
MPx =122
MPy = 44
mp_rect = mp.get_rect()
x = 226
while True:
    windowSurface.fill(BGCOLOR)
    now = pygame.time.get_ticks()
    lblRes = font.render(str(resource),1,(0,0,0))# show lable

    #changing of mp bar
    chop_rect = (0,0,x,0)
    crop_mp = pygame.transform.chop(mp,chop_rect)
    

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_d or event.key == K_a:
                marisa_animation.pause()
                marisa_animation = marisa_idle
                marisa_animation.play()
        if event.type == KEYDOWN: #  changing the type of mob     
            if event.key == K_RIGHT:
                current_mob+=1
                if current_mob > 3: 
                    current_mob = 1 

            if event.key == K_LEFT:
                current_mob-=1
                if current_mob < 1 : 
                    current_mob = 3
    mob_lower, mob_upper = type_mob[current_mob]
   
    
    keys = pygame.key.get_pressed()  #checking pressed keys
    mouse = pygame.mouse.get_pressed()

    for projectile in projectile_list:
        if projectile.rect.x > 1000:
            projectile_list.remove(projectile)


    """    
    x-axis left boundary, y-axis top boundary = 0
    x-axis right boundary = frame width - model width - 10
    y-axis bottom boundary = frame height - model height
    """
   
    if keys[pygame.K_UP]:
        if mamizou.rect.y > 0:
            mamizou.rect.y-=10
    if keys[pygame.K_DOWN]:
        if mamizou.rect.y < 530:
            mamizou.rect.y+=10
    if keys[pygame.K_a]:
        if marisa.rect.x>0:
            marisa_animation = marisa_forward
            marisa_animation.play()
            marisa.move_left()
    if keys[pygame.K_d]:
        if marisa.rect.x<914:
            marisa_animation = marisa_forward
            marisa_animation.play()
            marisa.move_right()         
    if keys[pygame.K_w]:
        if marisa.rect.y > 0:
            marisa.move_up()
    if keys[pygame.K_s]:
        if marisa.rect.y < 524:
            marisa.move_down()
    if keys[pygame.K_j]:
        if now - press_event >= rate:
            bullet = Bullet('marisa')
            bullet.rect.x = marisa.rect.x+76
            bullet.rect.y = marisa.rect.y+25
            projectile_list.add(bullet)
            press_event = pygame.time.get_ticks()
    if mouse[0]:
        if now - click_event >= mob_rate:
            if resource > 1000: #1000 is the cost of the mob
                mob = Mob('mob',mob_lower,mob_upper,0.25,3,'mob')
                sprites_list.add(mob)
                click_event = now
                resource -= 500


    resource+=5
    projectile_list.update()
    sprites_list.update()
    collide_list.update()

    collide_list = pygame.sprite.groupcollide(sprites_list, projectile_list, False, True)
    
    for sprite in collide_list:
        # print sprite 
        if sprite.ctype == 'character' or sprite.ctype == 'mob':
            sprite.hp -= 1
            if sprite.hp <= 0:
                x-=20
                if x < 0:
                    x = 226
                sprite.kill()
                #print sprite.hp

    for projectile in projectile_list:
        hit_list = pygame.sprite.spritecollide(projectile, sprites_list, False)
        for hit in hit_list:
            projectile_list.remove(projectile)
            sprites_list.remove(projectile)
    
    for sprite in sprites_list:
        if sprite.alive():
            sprite.animation2.blit(windowSurface, (sprite.rect.x, sprite.rect.y))
        else:
            sprite.animation2.blit(windowSurface, (sprite.rect.x, sprite.rect.y))

    
    projectile_list.draw(windowSurface)
    sprites_list.draw(windowSurface)
    windowSurface.blit(hp,(0,0))
    windowSurface.blit(crop_mp,(MPx,MPy)) #122 and 44
    windowSurface.blit(lblRes,(450,50))
    pygame.display.flip()
    pygame.display.update()
    
    mainClock.tick(30) # Feel free to experiment with any FPS setting.