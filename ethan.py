import pygame

pygame.init()

bgrdcol = (128, 128, 128)
lblcol = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

alive = 1
keycol = black
player_health = 100
heals = 10

x, y = 800, 600
window = pygame.display.set_mode((x, y))
font = pygame.font.Font('freesansbold.ttf', 32)

gun_sprite = pygame.image.load('guntest.png')
heal_sprite = pygame.image.load('swordtest.png')
heal_sprite = pygame.transform.scale(heal_sprite, (100, 100))
gun_sprite = pygame.transform.scale(gun_sprite, (100, 100))

show_inventory = False
labelmain = font.render('Inventory', True, lblcol)
labelrect = labelmain.get_rect(center=(x // 2, y // 4))
gun_rect = gun_sprite.get_rect(x=250, y=175)
heal_rect = heal_sprite.get_rect(x=450, y=175)

mapsprite = pygame.image.load('guntest.png')
mapsprite = pygame.transform.scale(mapsprite, (10000, 10000))
maprect = mapsprite.get_rect()

obstacles = [
    pygame.Rect(1120, 2080, 400, 80),  # Dark brown wall
    pygame.Rect(2880, 3520, 300, 400),  # Dark grey dungeon wall
    pygame.Rect(4800, 3520, 200, 600)  # Lava river
]

dungeon_door = pygame.Rect(2880, 3520, 50, 100)  # Define the dungeon door

obstacle_color = (0, 0, 0)
obstacles_visible = True

def toggle_obstacles():
    global obstacles_visible
    obstacles_visible = not obstacles_visible

def heal():
    global player_health, heals, alive, heallabel, healrect
    if heals > 0:
        if player_health <= 70:
            player_health += 30
        elif player_health == 80:
            player_health += 20
        elif player_health == 90:
            player_health += 10
        player_health = min(player_health, 100)
        heals -= 1
        heallabel = font.render(str(heals), True, black)
        healrect = heallabel.get_rect(center=(x // 1.5, y // 2.3))
        print(f"You have {heals} heals left")
        print(player_health)
    else:
        print("You have no heals left!")

    heallabel = font.render(str(heals), True, black)
    healrect = heallabel.get_rect(center=(x // 1.5, y // 2.3))


def draw_game_elements():
    window.blit(mapsprite, maprect)
    player_screen_position = player_rect.move(maprect.topleft)
    pygame.draw.rect(window, player_color, player_screen_position)
    if obstacles_visible:
        for obstacle in obstacles:
            obstacle_screen_position = obstacle.move(maprect.topleft)
            pygame.draw.rect(window, obstacle_color, obstacle_screen_position)

def draw_inventory():
    pygame.draw.rect(window, bgrdcol, pygame.Rect(180, 125, 450, 300))
    pygame.draw.rect(window, black, pygame.Rect(180, 125, 450, 300), 10)
    pygame.draw.rect(window, keycol, pygame.Rect(200, 300, 410, 100))
    window.blit(gun_sprite, gun_rect)
    window.blit(heal_sprite, heal_rect)
    window.blit(heallabel, healrect)
    window.blit(labelmain, labelrect)

def inv():
    global show_inventory
    show_inventory = True

def killinv():
    global show_inventory
    show_inventory = False

