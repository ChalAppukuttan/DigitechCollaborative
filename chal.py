import pygame
import random
import math

pygame.init()

# Window
# Tile types
G1 = 0
G2 = 1
G3 = 2

# Colors
GREEN1 = (50, 0, 252)
GREEN2 = (20, 50, 200)
GREEN3 = (20, 20, 250)

TileColour = {
    G1: GREEN1,
    G2: GREEN2,
    G3: GREEN3
}

mwidth = 200  # map width
mheight = 200  # map height
tilesize = 5

# Random Map Generator (RMG)
def RMG(w, h):
    return [[random.choice([G1, G2, G3]) for _ in range(mwidth)] for _ in range(mheight)]

Map1 = RMG(mwidth, mheight)

gw = pygame.display.set_mode((mwidth * tilesize, mheight * tilesize))
pygame.display.set_caption('Map')  # window name

def load_images(directory, a_name, a_num):
    return [pygame.image.load(f'{directory}/{a_name}{i}.png') for i in a_num]

# gooba sprite
still = load_images('JA', 'jstill', ['', '1', '2', '1'])
left = load_images('JA', 'jleft', ['1', '2', '3', '2'])
right = load_images('JA', 'jright', ['1', '2', '3', '2'])
up = load_images('JA', 'jup', ['1', '3', '4', '3'])
down = load_images('JA', 'jdown', ['1', '2', '4', '2'])

blue = load_images('JA', 'blue', [''])
kblue = load_images('JA', 'kblue', [''])

kstill = load_images('JA', 'kstill', ['', '1', '2', '1'])
kleft = load_images('JA', 'kleft', ['1', '2', '3', '2'])
kright = load_images('JA', 'kright', ['1', '2', '3', '2'])
kup = load_images('JA', 'kup', ['1', '3', '4', '3'])
kdown = load_images('JA', 'kdown', ['1', '2', '4', '2'])

still_rect = still[0].get_rect()
kstill_rect = kstill[0].get_rect()

still_rect.x = (random.randint(100, 500))  # random spawn on map
still_rect.y = (random.randint(100, 500))

kstill_rect.x = (random.randint(100, 500))  # random spawn on map
kstill_rect.y = (random.randint(100, 500))

moveleft = False
moveright = False
moveup = False
movedown = False

bluepower = False
kbluepower = False

kmoveleft = False
kmoveright = False
kmoveup = False
kmovedown = False
spd = 10
order = 0
korder = 0

clock = pygame.time.Clock()
LT = pygame.time.get_ticks()  # last updated time = # of ms
cdelay = 210  # cycle delay is 200 ms

# Enemy class
class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = speed

    def move_towards_player(self, player_rect):
        # Calculate the direction vector (dx, dy)
        dx, dy = player_rect.x - self.rect.x, player_rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        dx, dy = dx / distance, dy / distance

        # Move enemy towards the player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

# Enemy spawn variables
enemy_spawn_time = 3000  # in milliseconds
last_enemy_spawn_time = 0
enemies = []

# Game Loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw map
    for row in range(mheight):
        for col in range(mwidth):
            pygame.draw.rect(gw, TileColour[Map1[row][col]], (col * tilesize, row * tilesize, tilesize, tilesize))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and still_rect.left > 0 - 20:  # LEFT
        moveleft = True
        still_rect.x -= spd
        moveright = moveup = movedown = bluepower = False

    elif keys[pygame.K_d] and still_rect.right < mwidth * tilesize + 15:  # RIGHT
        moveright = True
        still_rect.x += spd
        moveleft = moveup = movedown = bluepower = False

    elif keys[pygame.K_w] and still_rect.top > 0 - 15:  # UP
        moveup = True
        still_rect.y -= spd
        moveleft = moveright = movedown = bluepower = False

    elif keys[pygame.K_s] and still_rect.bottom < mheight * tilesize + 0:  # DOWN
        movedown = True
        still_rect.y += spd
        moveleft = moveright = moveup = bluepower = False

    elif keys[pygame.K_g]:  # POWER
        bluepower = True
        moveup = moveleft = moveright = movedown = False

    else:
        moveleft = moveright = moveup = movedown = bluepower = False

    # Movement logic for character k
    if keys[pygame.K_LEFT] and kstill_rect.left > 0 - 20:  # LEFT
        kmoveleft = True
        kstill_rect.x -= spd
        kmoveright = kmoveup = kmovedown = False
    elif keys[pygame.K_RIGHT] and kstill_rect.right < mwidth * tilesize + 15:  # RIGHT
        kmoveright = True
        kstill_rect.x += spd
        kmoveleft = kmoveup = kmovedown = False
    elif keys[pygame.K_UP] and kstill_rect.top > 0 - 15:  # UP
        kmoveup = True
        kstill_rect.y -= spd
        kmoveleft = kmoveright = kmovedown = False
    elif keys[pygame.K_DOWN] and kstill_rect.bottom < mheight * tilesize:  # DOWN
        kmovedown = True
        kstill_rect.y += spd
        kmoveleft = kmoveright = kmoveup = False

    elif keys[pygame.K_y]:  # POWER
        kbluepower = True
        kmoveup = kmoveleft = kmoveright = kmovedown = False
    else:
        kmoveleft = kmoveright = kmoveup = kmovedown = kbluepower = False

    CT = pygame.time.get_ticks()  # current time = ticks
    if CT - LT > cdelay:  # if time is greater than the cycle delay
        order += 1
        korder += 1
        if order >= len(still):
            order = 0
        if korder >= len(kstill):
            korder = 0

        LT = CT

    # Spawn enemies
    if CT - last_enemy_spawn_time > enemy_spawn_time:
        enemy_x = random.randint(0, mwidth * tilesize)
        enemy_y = random.randint(0, mheight * tilesize)
        new_enemy = Enemy(enemy_x, enemy_y, 2)
        enemies.append(new_enemy)
        last_enemy_spawn_time = CT

    # Move and draw enemies
    for enemy in enemies:
        enemy.move_towards_player(still_rect)
        enemy.draw(gw)

    if moveleft:
        gw.blit(left[order], still_rect.topleft)
    elif moveright:
        gw.blit(right[order], still_rect.topleft)
    elif moveup:
        gw.blit(up[order], still_rect.topleft)
    elif movedown:
        gw.blit(down[order], still_rect.topleft)
    elif bluepower:
        gw.blit(blue[0], still_rect.topleft)
    else:
        gw.blit(still[order], still_rect.topleft)

    if kmoveleft:
        gw.blit(kleft[korder], kstill_rect.topleft)
    elif kmoveright:
        gw.blit(kright[korder], kstill_rect.topleft)
    elif kmoveup:
        gw.blit(kup[korder], kstill_rect.topleft)
    elif kmovedown:
        gw.blit(kdown[korder], kstill_rect.topleft)
    elif kbluepower:
        gw.blit(kblue[0], kstill_rect.topleft)
    else:
        gw.blit(kstill[korder], kstill_rect.topleft)

    clock.tick(100)
    pygame.display.update()

pygame.quit()
