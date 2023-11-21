import pygame
import random
from pygame.locals import *

pygame.font.init()

pygame.init()

#Tao cua so
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Space Shooter')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
#Scale BG bang man hinh:    
BG = pygame.transform.scale((pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\earth-1756274_640.webp')),(screen_width,screen_height))    
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

REPLAY = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\button_play.PNG') 
EXIT = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\button_exit.PNG')
START = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\button_play.PNG')
KEY_BINDINGS = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\button_keys.png')
BACK = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\button_back.png')
 
crash = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\crash.png') 
crash_rect = crash.get_rect()
 
font = pygame.font.SysFont("comicsans",40)
game_over_font = pygame.font.SysFont("comicsans",80)
title_font = pygame.font.SysFont("comicsans",60) 
score =0
hscore = 0


class Button:
    def __init__(self,x,y,image,scale):
        b_width = image.get_width()
        b_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(b_width*scale), int(b_height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return pygame.mouse.get_pressed()[0]
        else:
            return False
        
replay_buttom = Button(screen_width//3-100, screen_height//2-25,START,0.5) 
start_buttom = Button(screen_width//3-100, screen_height//2-25,START,0.5) 
quit_buttom = Button(2*screen_width//3-50, screen_height//2-25,EXIT,0.5) 
key_bindings_buttom = Button(250,450,KEY_BINDINGS,1)
back_buttom = Button(30,30,BACK,1)

class Buttom:
    def __init__(self,x,y,width,height,color,text):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.text = text
    def draw(self, surface):
        pygame.draw.rect(surface,self.color,self.rect)
        label = font.render(self.text, True, BLACK)
        surface.blit(label,(self.rect.x + self.rect.width//2 - label.get_width()//2,
                            self.rect.y + self.rect.height//2 - label.get_height()//2))
    #Ham check xem buttom co duoc nhan hay khong?
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return pygame.mouse.get_pressed()[0]
        else:
            return False
        

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
    def off_screen(self,height): # Ham Kiem tra xem vien dan da ra khoi man hinh hay chua
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
            laser.move(-vel) # Di chuyen laser
            if laser.off_screen(screen_height):# Neu laser bay ra khoi man hinh thi loai bo no
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):#kiem tra co ban trung ko
                        crash_rect.center = [obj.x,obj.y]
                        screen.blit(crash,(crash_rect))
                        objs.remove(obj)                      
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        global score
                        score += 1
    # Thanh Health bar
    def health_bar(self,screen):
        pygame.draw.rect(screen, RED, (self.x, self.y +self.ship_image.get_height()+10,self.ship_image.get_width(),5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y +self.ship_image.get_height()+10,self.ship_image.get_width() * (self.health/self.max_health),5))
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
        if self.cooldown_counter == 0:# Neu cooldown = 0 thi moi duoc ban.
            laser = Laser(self.x + self.get_width()/2-20, self.y, self.laser_image) #create laser o chinh giua ship cua player
            self.lasers.append(laser)
            self.cooldown_counter = 1 # Sau khi ban dat lai cooldown
# Ham kiem tra var cham:
def collide(object1,object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask,(offset_x,offset_y)) != None


def main_menu():
    title_font = pygame.font.SysFont("comicsans",60)
    run=True
    while run:
        screen.blit(BG,(0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                run= False
        start_buttom.draw(screen) # START BUTTOM
        quit_buttom.draw(screen) # EXIT BUTTOM
        key_bindings_buttom.draw(screen) #KEY BINDING BUTTOM
        if start_buttom.is_clicked(): # Neu nhan nut START thi bat dau
            main()
        if quit_buttom.is_clicked(): # Neu nhan nut Exit thi thoat ra
            run = False
        if key_bindings_buttom.is_clicked():
            key_bindings()
        pygame.display.update()
    pygame.quit() 

def key_bindings():
    run_key = True
    while run_key:
        screen.blit(BG,(0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
        A_txt = font.render("A: Move Left",1,(255,255,255))
        screen.blit(A_txt,(320,50))
        S_txt = font.render("S: Move Down",1,(255,255,255))
        screen.blit(S_txt,(320,150))
        D_txt = font.render("D: Move Right",1,(255,255,255))
        screen.blit(D_txt,(320,250))
        W_txt = font.render("W: Move Up",1,(255,255,255))
        screen.blit(W_txt,(320,350))
        Space_txt = font.render("Space: Shoot",1,(255,255,255))
        screen.blit(Space_txt,(320,450))
        back_buttom.draw(screen)
        if back_buttom.is_clicked():
            main_menu()
        pygame.display.update()
def main():
    running=True       
    clock=pygame.time.Clock()
    fps=120
    level = 0
    lives = 3
    gameOver = False
    enemies = []
    #number of enemies:
    wave_length = 0
    enemy_vel = 0.5
    laser_vel = 5
    enemy_laser_vel = 1
    player_vel = 4 #Van toc player
    player = Player(400,400)
    
    
    def draw_window():
        global score,hscore
        screen.blit(BG,(0,0))
        #draws level and lives:
        level_txt = font.render("Level: "+str(level),1,(255,255,255))
        screen.blit(level_txt,(10,10))
        lives_txt = font.render(f"Lives: {lives}",1,(255,255,255))
        screen.blit(lives_txt,(screen_width - lives_txt.get_width() - 10, 10))
        score_txt = font.render("SCORE: "+str(score),1,(255,255,255))
        screen.blit(score_txt,(250,10))
        #draws enemies:
        for enemy in enemies:
            enemy.draw(screen)
        #draws player's ship:
        player.draw(screen)
        #Neu Game Over thi in ra man hinh:
        if gameOver:
            screen.blit(BG,(0,0))
            gameOver_txt = game_over_font.render("You Lost",1,(255,255,255))
            screen.blit(gameOver_txt,((screen_width-gameOver_txt.get_width())/2,100))
            if score > hscore:
                hscore = score
            hscore_txt = font.render("High Score:"+str(hscore),1,(255,255,255))
            screen.blit(hscore_txt,(250,10))
            replay_buttom.draw(screen)
            quit_buttom.draw(screen)
            score = 0
            if replay_buttom.is_clicked(): # Neu nhan nut REPLAY thi bat dau lai
                main()
            if quit_buttom.is_clicked(): # Neu nhan nut Exit thi thoat ra
                quit() 
            
             
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
            player.score = 0
         
        if len(enemies) == 0:
            #Increase level and number of enemies:
            level += 1
            if level == 1:
                wave_length += 2
            wave_length += 3
            #Create random enemies:
            for i in range(wave_length):
                enemy =Enemy(random.randrange(100,screen_width-100),random.randrange(-1200*(level/5),-100))
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
                                          
main_menu()
  
    
    
        
        
        
        
        
        
        