import pygame
import random
import math

pygame.init()

# Window
# Tile types
C1 = 0
C2 = 1
C3 = 2

rcol = (255, 0, 0)
collrcol = (255, 255, 255)

# Colors
COL1 = (173, 173, 173)
COL2 = (133, 133, 133)
COL3 = (155, 155, 155)

TileColour = {
    C1: COL1,
    C2: COL2,
    C3: COL3
}

mwidth = 200  # map width
mheight = 200  # map height
tilesize = 5

# Enemy spawn variables
enemy_spawn_time = 3000  # in milliseconds
last_enemy_spawn_time = 0
enemies = []

# Random Map Generator (RMG)
def RMG(w, h):
    return [[random.choice([C1, C2, C3]) for _ in range(mwidth)] for _ in range(mheight)]

Map1 = RMG(mwidth, mheight)

pygame.init()
gw = pygame.display.set_mode((mwidth * tilesize, mheight * tilesize))
pygame.display.set_caption('Jelly Game')  # window name
running = True

def load_images(directory, a_name, a_num, colour):  # animation Name, animation Number #colour
    return [pygame.image.load(f'{directory}/{a_name}{i}{colour}.png') for i in a_num]

direct1 = 'RED'
player1col = direct1.lower()

direct2 = 'BLUE'
player2col = direct2.lower()

# gooba sprite
idle = load_images(direct1, 'idle', ['1', '2', '3', '2'], player1col)
left = load_images(direct1, 'left', ['1', '2', '3', '4', '3', '2'], player1col)
right = load_images(direct1, 'right', ['1', '2', '3', '4', '3', '2'], player1col)
up = load_images(direct1, 'up', ['1', '2', '3', '4', '3', '2'], player1col)
down = load_images(direct1, 'down', ['1', '2', '3', '4', '3', '2'], player1col)

light = load_images(direct1, 'light', ['1'], player1col)
light2 = load_images(direct2, 'light', ['1'], player2col)

idle2 = load_images(direct2, 'idle', ['1', '2', '3', '2'], player2col)
left2 = load_images(direct2, 'left', ['1', '2', '3', '2'], player2col)
right2 = load_images(direct2, 'right', ['1', '2', '3', '2'], player2col)
up2 = load_images(direct2, 'up', ['1', '3', '4', '3'], player2col)
down2 = load_images(direct2, 'down', ['1', '2', '4', '2'], player2col)

# adding a rock onto map :D
rock = load_images('bassest', 'rock', ['1'], 'rock')[0]

# scaling rock
rock_scaled = pygame.transform.scale(rock, (250, 250))

light_rect = light[0].get_rect()
light2_rect = light2[0].get_rect()
idle_rect = idle[0].get_rect()
idle2_rect = idle2[0].get_rect()

rock_rect = rock_scaled.get_rect()

idle_rect.x = random.randint(100, 500)  # random spawn on map
idle_rect.y = random.randint(100, 500)

idle2_rect.x = random.randint(100, 500)  # random spawn on map
idle2_rect.y = random.randint(100, 500)

rock_rect.x = random.randint(100, 700)
rock_rect.y = random.randint(100, 700)

rect_1 = pygame.Rect(0, 0, 25, 25)

pygame.mouse.set_visible(False)

moveleft = False
moveright = False
moveup = False
movedown = False

lightpower = False
lightpower2 = False

moveleft1 = False
moveright1 = False
moveup1 = False
movedown1 = False
spd = 7
order = 0
korder = 0

clock = pygame.time.Clock()
LT = pygame.time.get_ticks()  # last updated time = # of ms
cdelay = 210  # cycle delay is 200 ms

font = pygame.font.SysFont("Arial Bold", 36)
player1_name = font.render('Player 1', True, (0, 0, 0))
player2_name = font.render('Player 2', True, (0, 0, 0))

# Enemy class
class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = speed

    def move_towards_player(self, player1_rect, player2_rect):
        # Calculate the direction vector (dx, dy) towards the nearest player
        dx1, dy1 = player1_rect.x - self.rect.x, player1_rect.y - self.rect.y
        dx2, dy2 = player2_rect.x - self.rect.x, player2_rect.y - self.rect.y
        distance1 = math.hypot(dx1, dy1)
        distance2 = math.hypot(dx2, dy2)

        if distance1 < distance2:
            dx, dy = dx1, dy1
            distance = distance1
        else:
            dx, dy = dx2, dy2
            distance = distance2

        if distance == 0:
            return

        dx, dy = dx / distance, dy / distance

        # Move enemy towards the nearest player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

# Game Loop
run = True
while run:
    # Clear the screen
    gw.fill((0, 0, 0))

    # Spawn enemies
    CT = pygame.time.get_ticks()  # current time = ticks
    if CT - last_enemy_spawn_time > enemy_spawn_time:
        enemy_x = random.randint(0, mwidth * tilesize)
        enemy_y = random.randint(0, mheight * tilesize)
        new_enemy = Enemy(enemy_x, enemy_y, 2)
        enemies.append(new_enemy)
        last_enemy_spawn_time = CT
        print(f"Spawned new enemy at ({enemy_x}, {enemy_y})")



    # find cursor -> set rect position
    pos = pygame.mouse.get_pos()
    rect_1.center = pos

    # draw both rectangles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # draw map
    for row in range(mheight):
        for col in range(mwidth):
            pygame.draw.rect(gw, TileColour[Map1[row][col]], (col * tilesize, row * tilesize, tilesize, tilesize))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and idle_rect.left > 0 - 20:  # LEFT
        moveleft = True
        idle_rect.x -= spd
        moveright = moveup = movedown = lightpower = False

    elif keys[pygame.K_d] and idle_rect.right < mwidth * tilesize + 15:  # RIGHT
        moveright = True
        idle_rect.x += spd
        moveleft = moveup = movedown = lightpower = False

    elif keys[pygame.K_w] and idle_rect.top > 0 - 15:  # UP
        moveup = True
        idle_rect.y -= spd
        moveleft = moveright = movedown = lightpower = False

    elif keys[pygame.K_s] and idle_rect.bottom < mheight * tilesize + 0:  # DOWN
        movedown = True
        idle_rect.y += spd
        moveleft = moveright = moveup = lightpower = False

    elif keys[pygame.K_g]:  # POWER
        lightpower = True
        moveup = moveleft = moveright = movedown = False

    else:
        moveleft = moveright = moveup = movedown = lightpower = False

    # Movement logic for character k
    if keys[pygame.K_LEFT] and idle2_rect.left > 0 - 20:  # LEFT
        moveleft1 = True
        idle2_rect.x -= spd
        moveright1 = moveup1 = movedown1 = lightpower2 = False
    elif keys[pygame.K_RIGHT] and idle2_rect.right < mwidth * tilesize + 15:  # RIGHT
        moveright1 = True
        idle2_rect.x += spd
        moveleft1 = moveup1 = movedown1 = lightpower2 = False
    elif keys[pygame.K_UP] and idle2_rect.top > 0 - 15:  # UP
        moveup1 = True
        idle2_rect.y -= spd
        moveleft1 = moveright1 = movedown1 = lightpower2 = False
    elif keys[pygame.K_DOWN] and idle2_rect.bottom < mheight * tilesize:  # DOWN
        movedown1 = True
        idle2_rect.y += spd
        moveleft1 = moveright1 = moveup1 = lightpower2 = False

    elif keys[pygame.K_y]:  # POWER
        lightpower2 = True
        moveup1 = moveleft1 = moveright1 = movedown1 = False
    else:
        moveleft1 = moveright1 = moveup1 = movedown1 = lightpower2 = False

    CT = pygame.time.get_ticks()  # current time = ticks
    if CT - LT > cdelay:  # if time is greater than the cycle delay
        order += 1
        korder += 1
        if order >= len(idle):
            order = 0
        if korder >= len(idle2_rect):
            korder = 0

        LT = CT

    if moveleft:
        gw.blit(left[order], idle_rect.topleft)
    elif moveright:
        gw.blit(right[order], idle_rect.topleft)
    elif moveup:
        gw.blit(up[order], idle_rect.topleft)
    elif movedown:
        gw.blit(down[order], idle_rect.topleft)
    elif lightpower:
        gw.blit(light[0], idle_rect.topleft)
    else:
        gw.blit(idle[order], idle_rect.topleft)

    if moveleft1:
        gw.blit(left2[korder], idle2_rect.topleft)
    elif moveright1:
        gw.blit(right2[korder], idle2_rect.topleft)
    elif moveup1:
        gw.blit(up2[korder], idle2_rect.topleft)
    elif movedown1:
        gw.blit(down2[korder], idle2_rect.topleft)
    elif lightpower2:
        gw.blit(light2[0], idle2_rect.topleft)
    else:
        gw.blit(idle2[korder], idle2_rect.topleft)

    if rect_1.colliderect(idle_rect) or rect_1.colliderect(idle2_rect) or rect_1.colliderect(rock_rect):
        rcol = (255, 0, 0)
    else:
        rcol = (0, 255, 0)

    gw.blit(player1_name, (idle_rect.x, idle_rect.y - 30))
    gw.blit(player2_name, (idle2_rect.x, idle2_rect.y - 30))

    # draw the rock (ABOVE EVERYTHING ELSE)
    gw.blit(rock_scaled, rock_rect.topleft)  # Draw the scaled rock

    # draw the rectangle (ABOVE EVERYTHING ELSE)
    pygame.draw.rect(gw, rcol, rect_1)

    # Move and draw enemies
    for enemy in enemies:
        enemy.move_towards_player(idle_rect, idle2_rect)
        enemy.draw(gw)

    clock.tick(60)
    pygame.display.update()

# Quit Pygame
pygame.quit()
