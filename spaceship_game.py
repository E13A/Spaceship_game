import pygame
import random
import button
import math
from pygame import mixer
import time

start = time.time()

pygame.init()

screen = pygame.display.set_mode((960,720))
background = pygame.image.load("Space.jpg")

t = [0,9.98,29.97,59.97]
hiz = [0,30,50]

pygame.display.set_caption("Spaceship Game")
icon = pygame.image.load("ai.png")
pygame.display.set_icon(icon)

#load button images
left_img = pygame.image.load('leftb.png').convert_alpha()
right_img = pygame.image.load('rightb.png').convert_alpha()
target_img = pygame.image.load("target.png").convert_alpha()
exit_img = pygame.image.load("exit.png").convert_alpha()
start_img = pygame.image.load("Start.png").convert_alpha()

#create button instances
left_button = button.Button(50, 1750, left_img, 0.5)
right_button = button.Button(780, 1750, right_img, 0.5)
target_button = button.Button(430, 1800, target_img, 0.47)
exit_button = button.Button(340, 1000, exit_img, 0.8)
start_button = button.Button(340, 900, start_img, 0.8)

score_tab = 0
font = pygame.font.Font("freesansbold.ttf", 80)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 160)

player1Img = pygame.image.load("spaceship.png")
player1X = 480
player1Y = 1350
player1X_change = 6

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 1350
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"
newbulletImg = pygame.transform.scale(bulletImg,(70,70))

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
newenemyImg = []


for i in range (num_of_enemies):
	
	enemyImg.append(pygame.image.load("spaceship_enemy.png"))
	enemyX.append(random.randint(0,800))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(10)
	enemyY_change.append(130)
	newenemyImg.append(pygame.transform.scale(enemyImg[i], (190,190)))
	
	
def show_score(x,y):
	score=font.render("Score : " + str(score_tab), True, (255,255,255))
	screen.blit(score,(x,y))
	
def game_over():
	over_text=over_font.render("GAME OVER", True, (255,0,0))
	screen.blit(over_text,(50,800))

def player1(x,y):
	screen.blit(player1Img, (x, y))

def enemy(x,y,i):
	screen.blit(newenemyImg[i], (x, y))

def bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(newbulletImg, (x+60, y+10))
	
def isCollision(enemyX, enemyY, bulletX, bulletY, i):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) +(math.pow(enemyY-bulletY,2)) )
	if distance < 55:
		return True
	else:
		return False


running = True
while running:
	stop = time.time()

	screen.fill((0,0,0))
	screen.blit(background, (0,0))

	for y in range(len(t)):
		if (stop - start > (25+ t[y])) and (stop-start <( 25.1+t[y])):
			enemyImg.append(pygame.image.load("spaceship_enemy.png"))
			enemyX.append(random.randint(0,800))
			enemyY.append(random.randint(50,150))	
			enemyX_change.append(10)
			for v in range(len(hiz)):
				enemyY_change.append(130+hiz[v])
			newenemyImg.append(pygame.transform.scale(enemyImg[i], (190,190)))
		


	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if right_button.draw(screen):
		player1X_change = 6
	if left_button.draw(screen):
		player1X_change = -6
	if bullet_state is "ready":
		if target_button.draw(screen):
			bulletX = player1X
			bullet(bulletX, bulletY)
			bullet_sound = mixer.Sound("laser.wav")
			bullet_sound.play()
			
		
		
	if bullet_state is "fire":
		bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player1X += player1X_change
	
	
	if player1X <= 0:
		player1X = 970
	elif player1X >= 970:
		player1X = 0
		
	if bulletY <=0:
		bulletY = 1350
		bullet_state = "ready"
		
	for i in range(0,len(enemyImg)):
		if enemyY[i] > 1150:
			for j in range(0, len(enemyImg)):
				enemyY[j] = 4000
				player1Y = 4000
				left_button = button.Button(50, 4000, left_img, 0.5)
				right_button = button.Button(780, 4000, right_img, 0.5)
				target_button = button.Button(430, 4000, target_img, 0.47)
			game_over()
			textX = 375
			textY = 600
			if exit_button.draw(screen):
				running = False
			break
		
		enemyX[i] += enemyX_change[i]
	
		if enemyX[i] <= 0:
			enemyX_change[i] = 8
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 970:
			enemyX_change[i] = -8
			enemyY[i] += enemyY_change[i]
		
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY, i)
		if collision:
			bulletY = 1350
			bullet_state = "ready"
			score_tab += 1
			enemyX[i] = random.randint(0,800)
			enemyY[i] = random.randint(50,150)
		
		enemy(enemyX[i], enemyY[i],i)
	
		
	newplayer1Img = pygame.transform.scale(player1Img, (190,190))
	screen.blit(newplayer1Img, (player1X, player1Y))
	
	show_score(textX, textY)


		
	
	pygame.display.update()
print("bye")