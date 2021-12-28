# For more display variations visit www.flaticon.com and search spaceship
import pygame
import random
import math

# Initialize pygame(always there)
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

#Background Music(use mixer.music for long sounds)
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# PlayerIcon(consider size of image when deciding coordinates)
playerImg = pygame.image.load('player.png')
playerX = 384
playerY = 500
playerX_change = 0


def player(x, y):
    # blit draws the image on the object screen
    screen.blit(playerImg, (x, y))


# EnemyIcon(consider size of image when deciding coordinates)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
# enemyY_change=[]
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 737))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    # enemyY_change.append(0)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# BulletIcon(consider size of image when deciding coordinates)
# Ready - you cant see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX + 16
bulletY = 500
bulletY_change = 10
bullet_state = "ready"

#Game over
end_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    render=end_font.render("GAME OVER", True, (255,255,255))
    screen.blit(render, (200,250))

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

def show_score():
    render=font.render("Score :" + str(score), True, (255,255,255))
    screen.blit(render, (textX, textY))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX-bulletX)**2+(enemyY-bulletY)**2)
    if distance < 27:
        return True
    else:
        return False


# Game Loop
key = 0
running = True
while running:
    for event in pygame.event.get():
        # event = quit button
        if event.type == pygame.QUIT:
            running = False

        # check if keystrock is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                key = pygame.K_LEFT
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                key = pygame.K_RIGHT
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound= pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == key:
                playerX_change = 0
            else:
                pass

    # We want anything that persist in the game to be in the infinite running loop
    # screen.fill((0,0,0))
    screen.blit(background, (0, 0))

    # player movement
    # call only after the screen.fill() or playerimg will be under the screen
    # Making the addition here means that the x and y coordinate as long as the key is not released.
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    # enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i]> 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0 or enemyX[i] > 736:
            enemyX_change[i] *= -1
            enemyY[i] += 40

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound= pygame.mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 778)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #Display score
    show_score()
    # update the display. wont work if this line doesnt exist(mandatory)
    pygame.display.update()
