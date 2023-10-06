import pygame
import random
from pygame.locals import *
import math
import sys
import time
pygame.font.init()

pygame.init()

#Tao cua so
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Space Shooter')


#Scale BG bang man hinh:    
BG = pygame.transform.scale((pygame.image.load(r'E:\TUATUN\PYTHON GAME\Space_shooter\images\background.jpg')),(screen_width,screen_height))    
Player_ship =  pygame.image.load('E:\TUATUN\PYTHON GAME\Space_shooter\images\player.png')  
Enemy1 = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Space_shooter\images\enemy1_2.png')  
Enemy2 = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Space_shooter\images\enemy1_3.png')  
Enemy3 = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Space_shooter\images\enemy2_1.png')  
Enemy_Laser = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\bulletboss2.png')
LASER = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Space_shooter\images\bullet1.png')
LASER2 = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\bullet2.png')
LASER3 = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\bullet3.png')
LASER4 = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\bullet4.png')
Enemy_image = [Enemy1,Enemy2,Enemy3]
  
class Laser:
    def __init__(self,x,y,img):  
        self.x=x
        self.y=y
        self.img=img
        self.mask = pygame.mask.from_surface(self.img)
        
    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
    def move(self,vel):
        self.y += vel
    def off_screen(self,height):
        return self.y >= height or self.y<=0   
    def collision(self,object):
        return collide(object,self) #check var cham
        
class Ship:
    COOLDOWN = 60 #cooldown =0.5s vi fps=120
    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cooldown_counter = 0
    def draw(self,screen):
        screen.blit(self.ship_image,(self.x,self.y))
        #Draw laser:
        for laser in self.lasers:
            laser.draw(screen)
    def move_laser(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(screen_height):
                self.lasers.remove(laser)
            elif laser.collision(objs):#kiem tra co ban trung ko
                objs.health -= 10 #trung thi tru hp va remove laser
                self.lasers.remove(laser)
    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
    def shoot(self):
        if self.cooldown_counter == 0:# Neu cooldown =0 thi moi duoc ban.
            laser = Laser(self.x + self.get_width()/2-2, self.y, self.laser_image) #create laser o chinh giua ship cua player
            self.lasers.append(laser)
            self.cooldown_counter = 1 #Sau khi ban dat lai cooldown
            
    def get_width(self):
        return self.ship_image.get_width()
    def get_height(self):
        return self.ship_image.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = Player_ship
        self.laser_image = LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health
    def move_laser(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-vel)
            if laser.off_screen(screen_height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):#kiem tra co ban trung ko
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def health_bar(self,screen):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y +self.ship_image.get_height()+10,self.ship_image.get_width(),5))
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y +self.ship_image.get_height()+10,self.ship_image.get_width() * (self.health/self.max_health),5))
    def draw(self,screen):
        super().draw(screen)
        self.health_bar(screen)

class Enemy(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = random.choice(Enemy_image)
        self.laser_image = Enemy_Laser
        self.mask = pygame.mask.from_surface(self.ship_image)
    #moves enemy:
    def move(self, vel):
        self.y += vel
    def shoot(self):
        if self.cooldown_counter == 0:# Neu cooldown =0 thi moi duoc ban.
            laser = Laser(self.x + self.get_width()/2-20, self.y, self.laser_image) #create laser o chinh giua ship cua player
            self.lasers.append(laser)
            self.cooldown_counter = 1 #Sau khi ban dat lai cooldown
#Ham kiem tra var cham:
def collide(object1,object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask,(offset_x,offset_y)) != None
        
def main():
    running=True       
    clock=pygame.time.Clock()
    fps=120
    level = 0
    lives = 3
    gameOver = False
    font = pygame.font.SysFont("comicsans",40)
    game_over_font = pygame.font.SysFont("comicsans",80)

    enemies = []
    #number of enemies:
    wave_length = 0
    enemy_vel =0.5
    laser_vel = 5
    enemy_laser_vel =2
    player_vel = 4 #Van toc player
    player = Player(400,400)
    
    def draw_window():
        screen.blit(BG,(0,0))
        #draws level and lives:
        level_txt = font.render("Level: "+str(level),1,(255,255,255))
        screen.blit(level_txt,(10,10))
        lives_txt = font.render(f"Lives: {lives}",1,(255,255,255))
        screen.blit(lives_txt,(screen_width - lives_txt.get_width() - 10, 10))
        #draws enemies:
        for enemy in enemies:
            enemy.draw(screen)
        #draws player's ship:
        player.draw(screen)
        #Neu Game Over thi in ra man hinh:
        if gameOver:
            
            gameOver_txt = game_over_font.render("You Lost",1,(255,255,255))
            screen.blit(gameOver_txt,((screen_width-gameOver_txt.get_width())/2,(screen_height-gameOver_txt.get_height())/2))
             
        pygame.display.update()
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
        #Moving player:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:#LEFT
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() <screen_width:#RIGHT
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:#UP
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() +15 < screen_height:#DOWN
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        draw_window()
        #Dieu Kien Thua Game:
        if lives <=0 or player.health <=0:
            gameOver = True
            
        if len(enemies) == 0:
            #Increase level and number of enemies:
            level += 1
            wave_length += 5
            #Create random enemies:
            for i in range(wave_length):
                enemy =Enemy(random.randrange(50,screen_width-50),random.randrange(-1200*(level/5),-100))
                enemies.append(enemy)
        #Moving enemy:
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(enemy_laser_vel,player)
            #enemy ban dan:
            if random.randrange(0,120*4) == 1:
                enemy.shoot()
            if collide(enemy, player):#Neu Player var cham voi enemy thi -10hp va remove enemy
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > screen_height:
                lives -= 1 
                enemies.remove(enemy) #Remove enemy if enemy out of screen
            
        player.move_laser(laser_vel,enemies)
def main_menu():
    title_font = pygame.font.SysFont("comicsans",60)
    run=True
    while run:
        screen.blit(BG,(0,0))
        title_txt = title_font.render("Press the buttom to begin...",1,(255,255,255))
        screen.blit(title_txt,(screen_width/2-title_txt.get_width()/2,screen_height/2-title_txt.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run= False
            if event.type == MOUSEBUTTONDOWN:
                main()      
    pygame.quit() 
                                  
main_menu()
    
    
    
        
        
        
        
        
        
        