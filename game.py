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
game_flag = True
skill_press = False
skill_rate = 1500
victory = False
victory_event = 0

#set up the window
windowSurface = pygame.display.set_mode((1024, 600))
pygame.display.set_caption('Project Touhou: Minus 1.0')
background = pygame.image.load('UI/game_bg.png')


#create the list of sprites
projectile_list =  pygame.sprite.Group()
sprites_list = pygame.sprite.Group()
collide_list = pygame.sprite.Group()
skill_collide = pygame.sprite.Group()
mob_list = pygame.sprite.Group()
deco_list = pygame.sprite.Group()
skill_list = pygame.sprite.Group()

#instantiate ui's
container_p1 = pygame.image.load('UI/marisa_hp.png').convert_alpha()
container_p2 = pygame.image.load('UI/mamizou_hp.png').convert_alpha()
pointer  = pygame.image.load('UI/summon_pointer.png').convert_alpha()
timer_bg  = pygame.image.load('UI/time_bg.png').convert_alpha()
mob_normal_cd  = pygame.image.load('UI/mob_cd_blank.png').convert_alpha()
mob_large_cd  = pygame.image.load('UI/mob_cd_blank.png').convert_alpha()
charge_1 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
charge_2 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
charge_3 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
pointer_index = 671 #position of small mob

mp = pygame.image.load('UI/mp.png').convert_alpha()
p1_hp = pygame.image.load('UI/health_bar.png')
p2_hp = pygame.image.load('UI/health_bar.png')
frame = 0 # for timer countdown
shoot_win = pygame.image.load('UI/shooter_win.png').convert_alpha()
def_win = pygame.image.load('UI/defender_win.png').convert_alpha()
draw_win = pygame.image.load('UI/draw.png').convert_alpha()


#instantiate sprites
marisa = Marisa('marisa',332,345,0.05, 30,'character')
mamizou = Mamizou('mamizou',1,15,0.09,50,'character')
laser = Character('skill',11,18,0.025,90,'character')

#add each sprite inside the list of sprites for hitbox checking
sprites_list.add(marisa)
sprites_list.add(mamizou)
deco_list.add(laser)


marisa_idle = marisa.animate(332, 345, 0.05)
marisa_forward = marisa.animate(4120, 4127, 0.05)
marisa_animation = marisa_idle


# Projectile Animation for marisa
press_event  = 0
skill_press_event = 0
snow = 0
rate = 300
time = 180

#mob respawn rate 
click_event = 0
mob_rate = 300
resource = 500
cd_normal = 2500 #cooldown for normal mob
cd_large = 5000  # coooldown for large mob

#---------------------------------

#mob indices
type_mob = {1:(0,1),2:(2,3),3:(4,5)}
current_mob = 1


#printing of label
font = pygame.font.Font("UI/HighlandGothicFLF.ttf", 25)
time_f = pygame.font.Font("UI/HighlandGothicFLF.ttf", 40)

marisa_animation.play()
mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)
cooldown = 1

#---------------------------------

#animationn of hp and mp bars

x = 226
x_p1 = 0
x_p2 = 0
charges = 0

while game_flag:

    windowSurface.blit(background,(0,0))
    now = pygame.time.get_ticks()
    now2 = pygame.time.get_ticks()
    lblRes = font.render(str(resource),1,(255,255,100))# show label
    lblTime = time_f.render(str(time),1,(255,255,255))# show label
    
    #changing of hp and mp bar
    chop_rect = (0,0,x,0)
    chop_p1 = (0,0,x_p1,0)
    chop_p2 = (0,0,x_p2,0)

    crop_mp = pygame.transform.chop(mp,chop_rect)
    crop_hp1 = pygame.transform.chop(p1_hp,chop_p1)
    crop_hp2 = pygame.transform.chop(p2_hp,chop_p2)

    #decreases the timer on screen
    frame+=1
    if frame == 30: # 30 = 1 sec
        time-=1
        frame = 0
    if charges == 3:
        x = 226    

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            game_flag = False       
        if event.type == KEYUP and skill_press == False:
            if event.key == K_d:# or event.key == K_j or event.key == K_k:
                marisa.animation2 = marisa.animate(332,345,0.05)
                marisa.animation2.play()
                # marisa_animation.pause()
                # marisa_animation = marisa_idle
                # marisa_animation.play()
        if event.type == KEYDOWN: #  changing the type of mob     
            if event.key == K_RIGHT:
                current_mob+=1
                pointer_index+=70
                if current_mob > 3: 
                    current_mob = 1
                    pointer_index = 671 # reset to the first type of mob
            if event.key == K_d and skill_press == False:                
                marisa.animation2 = marisa.animate(4120,4127,0.05)
                marisa.animation2.play()

            # if event.key == K_j:
            #     marisa.animation2 = marisa.animate(125,129,0.1)
            #     marisa.animation2.play()

            if event.key == K_LEFT:
                current_mob-=1
                pointer_index-=70
                if current_mob < 1 : 
                    current_mob = 3
                    pointer_index = 811 # move to the last type of mob
            print current_mob
    mob_lower, mob_upper = type_mob[current_mob]
       
    keys = pygame.key.get_pressed()  #checking pressed keys and mousebuttons
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
            marisa.move_left()
    if keys[pygame.K_d] and skill_press == False:
        if marisa.rect.x<914 and marisa.rect.x < 456:
            marisa.move_right()         
    if keys[pygame.K_w] and skill_press == False:
        if marisa.rect.y > 80:
            marisa.move_up()
    if keys[pygame.K_s] and skill_press == False:
        if marisa.rect.y < 524:
            marisa.move_down()
    if keys[pygame.K_j] and skill_press == False:
        if now - press_event >= rate:
            if marisa.alive():
                bullet = Bullet('marisa','character',1)
                bullet.rect.x = marisa.rect.x+76
                bullet.rect.y = marisa.rect.y+25
                projectile_list.add(bullet)
                skill_press = False
            press_event = pygame.time.get_ticks()
    if keys[pygame.K_k] and skill_press == False:
        if now - skill_press_event >= 1500:
            if marisa.alive() and charges > 0:
               skill_press = True
               marisa.animation2 = marisa.animate(128,129,0.1)
               marisa.animation2.play()
               skill = Bullet('marisa', 'skill', 0.2, True)
               skill.rect.x = marisa.rect.x+90
               skill.rect.y = marisa.rect.y+15
               laser.rect.x = marisa.rect.x + 90
               laser.rect.y = marisa.rect.y - 85
               skill_list.add(skill)
               x = 226
               charges-=1
            skill_press_event = pygame.time.get_ticks()

    #summonning of mobs
    if mouse[0] and mamizou.alive():
        if now - click_event >= mob_rate and pygame.mouse.get_pos()[0] >= 556 and pygame.mouse.get_pos()[1] >= 100:
            if current_mob == 1 and resource >= 150:
                mob = Mob('small',0,1,0.25,3,'mob')
                resource -= 150
                click_event = now
            if now - click_event >= cd_normal and current_mob == 2 and resource >= 250:
                mob = Mob('normal',0,1,0.25,6,'mob')
                resource -= 250
                click_event = now
                mob_normal_cd  = pygame.image.load('UI/mob_cd_fill.png').convert_alpha()
            if now - click_event >= cd_large and current_mob == 3 and resource >= 400:
                mob = Mob('large',0,1,0.25,15,'mob')
                resource -= 400
                click_event = now
                mob_large_cd  = pygame.image.load('UI/mob_cd_fill.png').convert_alpha()
            
            sprites_list.add(mob)
            mob_list.add(mob)
    #removing cooldownz
    if now - click_event >= cd_normal:
        mob_normal_cd  = pygame.image.load('UI/mob_cd_blank.png').convert_alpha()
    if now - click_event >= cd_large:
        mob_large_cd  = pygame.image.load('UI/mob_cd_blank.png').convert_alpha()
            
            
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
    deco_list.update()
    skill_list.update()

   #pierce skill
    skill_collide2 = pygame.sprite.groupcollide(skill_list, sprites_list, False, False)
    for projectile in skill_collide2:
        skill_dmg = projectile.dmg

    #projectiles
    skill_collide = pygame.sprite.groupcollide(sprites_list, skill_list, False, False)
    for sprite in skill_collide:
        if sprite.ctype == 'character' or sprite.ctype == 'mob':
            sprite.hp -= skill_dmg
            print sprite.hp
            if sprite.fname=='marisa':
                if marisa.hp> 1:
                    x_p1 = x_p1 + 306/(30/skill_dmg)# 30 is the full hp of marisa
                if marisa.hp <=1:
                    x_p1 += x_p1
            if sprite.fname== 'mamizou':
                if mamizou.hp> 1:
                    x_p2 = x_p2 + 306/(50/skill_dmg)#50 full hp of mamizou
                if mamizou.hp <= 1:
                    x_p2 += x_p2
            if sprite.hp <= 0:
                if sprite.ctype == 'mob':
                        x-=20
                if x <= 0:
                    x = 226
                sprite.kill()
                #hello
     
    
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
            x -= 5
            if x <= 0:
                x = 226
                if charges <= 3:
                    charges+=1
            if sprite.fname=='marisa':
                if marisa.hp> 1:
                    x_p1 = x_p1 + 306/(30/dmg)# 30 is the full hp of marisa
                if marisa.hp <1:
                    x_p1 += x_p1
            if sprite.fname== 'mamizou':
                if mamizou.hp> 1:
                    x_p2 = x_p2 + 306/(50/dmg)#50 full hp of mamizou
                if mamizou.hp < 1:
                    x_p2 += x_p2
            if sprite.hp <= 0:
                if sprite.ctype == 'mob' and mob.fname == 'small':
                        x-=20
                if sprite.ctype == 'mob' and mob.fname == 'normal':
                        x-=30
                if sprite.ctype == 'mob' and mob.fname == 'large':
                        x-=50
                if x < 0:
                    if charges <= 3:
                        charges+=1
                    x = 266
                sprite.kill()
    if charges == 0:
        charge_1 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
        charge_2 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
        charge_3 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
    if charges == 1:
        charge_1 = pygame.image.load('UI/skill_charge.png').convert_alpha()
        charge_2 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
        charge_3 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
    if charges == 2:
        charge_1 = pygame.image.load('UI/skill_charge.png').convert_alpha()
        charge_2 = pygame.image.load('UI/skill_charge.png').convert_alpha()
        charge_3 = pygame.image.load('UI/skill_charge_empty.png').convert_alpha()
    if charges == 3:
        charge_1 = pygame.image.load('UI/skill_charge.png').convert_alpha()
        charge_2 = pygame.image.load('UI/skill_charge.png').convert_alpha()
        charge_3 = pygame.image.load('UI/skill_charge.png').convert_alpha()
             
    
    #check if sprite is alive (hp != 0)
    #play appropriate animation
    for sprite in sprites_list:
        if sprite.alive():
            sprite.animation2.blit(windowSurface, (sprite.rect.x, sprite.rect.y))
        else:
            sprite.animation.blit(windowSurface, (sprite.rect.x, sprite.rect.y))

    #skill animation
    if skill_press == True:
        laser.animation2.blit(windowSurface, (marisa.rect.x+90,marisa.rect.y-85))
        if now - skill_press_event > skill_rate:
            marisa.animation2 = marisa.animate(332,345,0.05)
            marisa.animation2.play()
            skill_press = False
            skill_list.remove(skill)   


    skill_list.draw(windowSurface)
    projectile_list.draw(windowSurface)
    sprites_list.draw(windowSurface)
    deco_list.draw (windowSurface)
    windowSurface.blit(container_p1,(0,0))
    windowSurface.blit(container_p2,(583,0))
    windowSurface.blit(timer_bg,(447.5,0))
    windowSurface.blit(pointer,(pointer_index,60)) #673 = small, 742 = normal
    windowSurface.blit(mob_normal_cd,(737,40)) #cooldown locations 737 = normal, 803 = large
    windowSurface.blit(mob_large_cd,(803,40)) #cooldown locations 737 = normal, 803 = large
    windowSurface.blit(charge_1,(360,50))
    windowSurface.blit(charge_2,(385,50))
    windowSurface.blit(charge_3,(410,50))
    windowSurface.blit(crop_hp1,(125,22))
    windowSurface.blit(crop_hp2,(591 + x_p2,22))
    windowSurface.blit(crop_mp,(122,44)) #122 and 44
    windowSurface.blit(lblRes,(600,50))
    windowSurface.blit(lblTime,(478,-3))

    #check for victor
    if not marisa.alive():
        windowSurface.blit(def_win, (0,200))
    if not mamizou.alive():
        windowSurface.blit(shoot_win, (0,200))
        print now - victory_event
    if not marisa.alive() and not mamizou.alive():
        windowSurface.blit(draw_win, (0,200))
        
    pygame.display.flip()
    pygame.display.update()
    
    mainClock.tick(30) # Feel free to experiment with any FPS setting.