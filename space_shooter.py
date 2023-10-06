import pygame
import random
from pygame.locals import *
import math

clock=pygame.time.Clock()
fps=120
pygame.init()

#Tao cua so
width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Space Shooter')

font = pygame.font.Font(pygame.font.get_default_font(),20)
game_over_font = pygame.font.Font(pygame.font.get_default_font(),60)
#Show score va Gameover
def score_view(x,y):
    score_txt = font.render('Score: '+str(score),True,(255,255,255))
    screen.blit(score_txt, (x,y))
def game_over_view():
    game_over_text=game_over_font.render('GAME OVER',True,(255,255,255))
    game_over_text_rect=game_over_text.get_rect()
    game_over_text_rect.center=(400,300)
    screen.blit(game_over_text,game_over_text_rect)
    hscore_txt=font.render('High Score: '+str(hscore),True,(255,255,255))
    hscore_txt_rect=hscore_txt.get_rect()
    hscore_txt_rect.center=(400,150)
    screen.blit(hscore_txt,hscore_txt_rect)
    
gameOver = False
score, hscore = 0, 0


#Load hinh anh player:
playerImage = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\player.png')
player_x = 370
player_y = 523
player_x_change = 0
#Load hinh anh Invader vao 1 list:
invader_x=[]
invader_y=[]
invader_x_change=[]
invader_y_change=[]
invader_images = []
no_of_invader = 8
for num in range(no_of_invader):
    invader_images.append(pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\enemy1_2.png'))
    invader_x.append(random.randint(64,737))
    invader_y.append(random.randint(30,180))
    invader_x_change.append(1.2)
    invader_y_change.append(100)

    
#Load hinh danh bullet:
bulletImage = pygame.image.load(r'E:\TUATUN\PYTHON GAME\Game_ban_tau\images\bullet1.png')
bullet_x = 0
bullet_y = 500
bullet_x_change=0
bullet_y_change=3
#trang thai dan: rest la dung yen/ fire la dang ban
bullet_state = "rest"

#ve player:
def draw_player(x,y):
    screen.blit(playerImage,(x-16,y+10))
#ve invader:
def draw_invader(x,y,i):
    screen.blit(invader_images[i],(x,y))
#ve bullet:
def draw_bullet(x,y):
    global bullet_state
    screen.blit(bulletImage,(x,y))
    bullet_state = 'fire'
#ham chack va cham:
def isCollision(x1,x2,y1,y2):
    distance = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
    if distance <= 50:
        return True
    else:
        return False

running = True
while running:
    clock.tick(fps)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        #dieu khien player:
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_x_change = -1.7
            if event.key == K_RIGHT:
                player_x_change = 1.7
            if event.key == K_SPACE:
                if bullet_state is 'rest':
                    bullet_x = player_x + 29
                    draw_bullet(bullet_x,bullet_y)
        if event.type == KEYUP:
            player_x_change = 0
    #Cap nhat vi tri cua player:
    player_x += player_x_change
    #Cap nhat bullet di chuyen:
    if bullet_y <0 :
        bullet_y=600
        bullet_state='rest'
    if bullet_state is 'fire':
        draw_bullet(bullet_x,bullet_y) 
        bullet_y -= bullet_y_change
    #Ve invader di chuyen:
    for i in range(no_of_invader):
        invader_x[i] += invader_x_change[i]
        if invader_y[i] >=450:
            if abs( player_x-invader_x[i])<80:
                for j in range(no_of_invader):
                    invader_y[j]=2000
                game_over_view()
                break
        if invader_x[i] >= 735 or invader_x[i] <= 0:
            invader_x_change[i] *= -1
            invader_y[i] += invader_y_change[i]
        #Collision/va cham
        collision = isCollision(bullet_x,invader_x[i],bullet_y,invader_y[i])  
        if collision:
            score+=1
            if score>hscore:
                hscore=score
            bullet_y =600
            bullet_state = 'rest'
            invader_x[i]=random.randint(64,737)
            invader_y[i]=random.randint(30,180)
            invader_x_change[i] *= -1
        
        draw_invader(invader_x[i],invader_y[i],i)
    #khong cho player di ra khoi man hinh:
    if player_x <= 16:
        player_x = 16
    if player_x >=750:
        player_x =750      
    draw_player(player_x,player_y)
    score_view(5,5)
    pygame.display.update()


