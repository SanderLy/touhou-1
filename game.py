import pygame
import sys
import time
import pyganim
import os
import random
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
background = pygame.image.load('UI/game_bg.png')


#misc initializations
skill_press = False

#create the list of sprites
projectile_list =  pygame.sprite.Group()
sprites_list = pygame.sprite.Group()
collide_list = pygame.sprite.Group()
mob_list = pygame.sprite.Group()
skill_list = pygame.sprite.Group()

#instantiate ui's
container_p1 = pygame.image.load('UI/marisa_hp.png').convert_alpha()
container_p2 = pygame.image.load('UI/mamizou_hp.png').convert_alpha()
mp = pygame.image.load('UI/mp.png').convert_alpha()
p1_hp = pygame.image.load('UI/health_bar.png')
p2_hp = pygame.image.load('UI/health_bar.png')


#instantiate sprites
marisa = Marisa('marisa',332,345,0.05, 30,'character')
mamizou = Mamizou('mamizou',1,15,0.09,50,'character')
laser = Character('skill',11,18,0.05,1,'character')

#add each sprite inside the list of sprites for hitbox checking
sprites_list.add(marisa)
sprites_list.add(mamizou)


marisa_idle = marisa.animate(332, 345, 0.05)
marisa_forward = marisa.animate(4120, 4127, 0.05)
marisa_animation = marisa_idle


# Projectile Animation for marisa

press_event  = 0
snow = 0
rate = 300
time = 180
#---------------------------------

#mob respawn rate 

click_event = 0
mob_rate = 300

resource = 500

#---------------------------------

#mob indices
type_mob = {1:(0,1),2:(2,3),3:(4,5)}
current_mob = 1


#printing of label
font = pygame.font.Font(None, 35)
time_f = pygame.font.Font(None, 50)

marisa_animation.play()
mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)
cooldown = 1

#---------------------------------

#animationn of hp and mp bars

x = 226
x_p1 = 0
x_p2 = 0

while True:

    windowSurface.blit(background,(0,0))
    now = pygame.time.get_ticks()
    lblRes = font.render(str(resource),1,(255,255,100))# show label
    lblTime = time_f.render(str(time),1,(200,70,25))# show label
    
    #changing of hp and mp bar
    chop_rect = (0,0,x,0)
    chop_p1 = (0,0,x_p1,0)
    chop_p2 = (0,0,x_p2,0)

    crop_mp = pygame.transform.chop(mp,chop_rect)
    crop_hp1 = pygame.transform.chop(p1_hp,chop_p1)
    crop_hp2 = pygame.transform.chop(p2_hp,chop_p2)
    

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
        if projectile.rect.x > 1000 or projectile.rect.x < 0:
            projectile_list.remove(projectile)


    """    
    x-axis left boundary, y-axis top boundary = 0
    x-axis right boundary = frame width - model width - 10
    y-axis bottom boundary = frame height - model height
    """
   
    if keys[pygame.K_UP]:
        if mamizou.rect.y > 80:
            mamizou.rect.y-=10
    if keys[pygame.K_DOWN]:
        if mamizou.rect.y < 530:
            mamizou.rect.y+=10
    if keys[pygame.K_a] and skill_press == False:
        if marisa.rect.x>0:
            marisa_animation = marisa_forward
            marisa_animation.play()
            marisa.move_left()
    if keys[pygame.K_d] and skill_press == False:
        if marisa.rect.x<914 and marisa.rect.x < 456:
            marisa_animation = marisa_forward
            marisa_animation.play()
            marisa.move_right()         
    if keys[pygame.K_w] and skill_press == False:
        if marisa.rect.y > 80:
            marisa.move_up()
    if keys[pygame.K_s] and skill_press == False:
        if marisa.rect.y < 524:
            marisa.move_down()
    if keys[pygame.K_j]:
        if now - press_event >= rate:
            if marisa.alive():
                bullet = Bullet('marisa','character',1)
                bullet.rect.x = marisa.rect.x+76
                bullet.rect.y = marisa.rect.y+25
                projectile_list.add(bullet)
            press_event = pygame.time.get_ticks()
    if keys[pygame.K_k]:
        if now - press_event >= 1500:
            if marisa.alive() and x == 0:
                skill_press = True
                skill = Bullet('marisa','skill',0.25,True)
                skill.rect.x = marisa.rect.x+80
                skill.rect.y = marisa.rect.y-75
                laser.rect.x = marisa.rect.x+80
                laser.rect.y = marisa.rect.y-75
                skill_list.add(skill)
            press_event = pygame.time.get_ticks()

    if mouse[0] and mamizou.alive():
        if now - click_event >= mob_rate and pygame.mouse.get_pos()[0] >= 556:
            if current_mob == 1 and resource >= 150:
                mob = Mob('small',0,1,0.25,3,'mob')
                resource -= 150
            if current_mob == 2 and resource >= 250:
                mob = Mob('normal',0,1,0.25,6,'mob')
                resource -= 250
            if current_mob == 3 and resource >= 400:
                mob = Mob('large',0,1,0.25,15,'mob')
                resource -= 400
            sprites_list.add(mob)
            mob_list.add(mob)
            click_event = now
            
    for mob in mob_list:
            if mob.fname == 'small':
                bullet_mob = Bullet('small','mob')
                bullet_mob.rect.x = mob.rect.x - 10
                bullet_mob.rect.y = mob.rect.y + 35
                rand = random.randint(8,15)

            if mob.fname == 'normal':
                bullet_mob = Bullet('normal','mob',2)
                bullet_mob.rect.x = mob.rect.x - 75
                bullet_mob.rect.y = mob.rect.y + 35
                rand = random.randint(7,15)

            if mob.fname == 'large':
                bullet_mob = Bullet('large','mob',3)
                bullet_mob.rect.x = mob.rect.x - -50
                bullet_mob.rect.y = mob.rect.y + 110
                rand = random.randint(6,15)

            if now - mob.last_fire >= rand * 100:
                projectile_list.add(bullet_mob)
                mob.last_fire = now

    #resource increase per tick
    resource+=1

    #update for sprite lists
    projectile_list.update()
    sprites_list.update()
    collide_list.update()
    skill_list.update()

     #pierce skill
    skill_collide2 = pygame.sprite.groupcollide(skill_list, sprites_list, False, False)
    for projectile in skill_collide2:
        skill_dmg = projectile.dmg
    skill_collide = pygame.sprite.groupcollide(sprites_list, skill_list, False, False)
    for sprite in skill_collide:
        if sprite.ctype == 'character' or sprite.ctype == 'mob':
            sprite.hp -= skill_dmg
            print sprite.hp
            if sprite.fname=='marisa':
                if marisa.hp> 1:
                    x_p1 = x_p1 + 306/(30/skill_dmg)# 30 is the full hp of marisa
                if marisa.hp ==1:
                    x_p1 += x_p1
            if sprite.fname== 'mamizou':
                if mamizou.hp> 1:
                    x_p2 = x_p2 + 306/(50/skill_dmg)#50 full hp of mamizou
                if mamizou.hp ==1:
                    x_p2 += x_p2
            if sprite.hp <= 0:
                if sprite.ctype == 'mob':
                        x-=20
                if x < 0:
                    x = 226
                sprite.kill()

    
    #sets damage of colliding projectile
    collide_list2 = pygame.sprite.groupcollide(projectile_list, sprites_list, False, False)
    for projectile in collide_list2:
        dmg = projectile.dmg

   
    #returns a dictionary{[sprites_list]:[projectile_list]}
    collide_list = pygame.sprite.groupcollide(sprites_list, projectile_list, False, True)

    #check sprite if character or mob
    #checks if a sprite hits 0 hp per collide
    for sprite in collide_list:
        if sprite.ctype == 'character' or sprite.ctype == 'mob':
            sprite.hp -= dmg
            if sprite.fname=='marisa':
                print "dmg: " + str(dmg)
                if marisa.hp> 1:
                    x_p1 = x_p1 + 306/(30/dmg)# 30 is the full hp of marisa
                if marisa.hp <1:
                    x_p1 += x_p1
            if sprite.fname== 'mamizou':
                if mamizou.hp> 1:
                    x_p2 = x_p2 + 306/(50/dmg)#50 full hp of mamizou
                if mamizou.hp <1:
                    x_p2 += x_p2
            print mamizou.hp
            if sprite.hp <= 0:
                if sprite.ctype == 'mob' and mob.fname == 'small':
                        x-=20
                if sprite.ctype == 'mob' and mob.fname == 'normal':
                        x-=30
                if sprite.ctype == 'mob' and mob.fname == 'large':
                        x-=50
                if x < 0:
                    x = 0
                sprite.kill()
    
    #check if sprite is alive (hp != 0)
    #play appropriate animation
    for sprite in sprites_list:
        if sprite.alive():
            sprite.animation2.blit(windowSurface, (sprite.rect.x, sprite.rect.y))
        else:
            sprite.animation.blit(windowSurface, (sprite.rect.x, sprite.rect.y))

    if len(skill_list) > 0:
        if now - press_event > 1000:
            skill_list.remove(skill)
            skill_press = False
            x = 226 # reset mp to empty
    if skill_press == True:
        sprites_list.add(laser)

    projectile_list.draw(windowSurface)
    sprites_list.draw(windowSurface)
    skill_list.draw(windowSurface)
    windowSurface.blit(container_p1,(0,0))
    windowSurface.blit(container_p2,(583,0))
    windowSurface.blit(crop_hp1,(125,22))
    windowSurface.blit(crop_hp2,(591,22))
    windowSurface.blit(crop_mp,(122,44)) #122 and 44
    windowSurface.blit(lblRes,(600,50))
    windowSurface.blit(lblTime,(480,20))
    pygame.display.flip()
    pygame.display.update()
    
    mainClock.tick(30) # Feel free to experiment with any FPS setting.