import pygame
from pygame import *

pygame.init()

width, height = 640, 240
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))

base_loc = './resources/'
player = pygame.image.load(base_loc + "stand.png")
player_left = pygame.image.load(base_loc + "stand_left.png")
player_shoot = pygame.image.load(base_loc + "shoot.png")
player_shoot_left = pygame.image.load(base_loc + "shoot_left.png")

rect = player.get_rect()
rect.bottom = height
rect.left = 0

delta = [0, 0]
speed = 2.0

gravity = 10.0
jump_speed = 6.0

key_stats = {'w_down': False,
             'a_down': False,
             'd_down': False,
             'a_time': -1,
             'd_time': -1,
             'j_down': False}

stats = {'moving': 'stand',
         'forward': 'right',
         'shooting': False,
          'jumping': False}

def get_vy(t):
    vy = jump_speed - gravity*t
    return vy

def detect_key_stats(event):
    global key_stats
    if event.type == pygame.KEYDOWN:
        if event.key == K_w:
            key_stats['w_down'] = True
        if event.key == K_a:
            key_stats['a_down'] = True
            key_stats['a_time'] = time
        if event.key == K_d:
            key_stats['d_down'] = True
            key_stats['d_time'] = time
        if event.key == K_j:
            key_stats['j_down'] = True
    if event.type == pygame.KEYUP:
        if event.key == K_w:
            key_stats['w_down'] = False
        if event.key == K_a:
            key_stats['a_down'] = False
        if event.key == K_d:
            key_stats['d_down'] = False
        if event.key == K_j:
            key_stats['j_down'] = False

def limit_in_view():
    global rect
    if rect.left < 0:
        rect.left = 0
    if rect.right > width:
        rect.right = width
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > height:
        rect.bottom = height

# Useless
blue = 0
reverse = False
def useless_background():
    global blue
    global reverse
    if blue == 100:
        reverse = False
    if blue == 150:
        reverse = True
    if reverse:
        blue -= 1
    else:
        blue += 1

running = True
time = 0
jump_time = 0

while running:
    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            running = False
        # Detect the key event
        detect_key_stats(event)

    delta = [0, 0]

    #Shoot! Shoot!!!
    if key_stats['j_down']:
        stats['shooting'] = True
    else:
        stats['shooting'] = False

    # Jump! Jump! Jump!
    if key_stats['w_down'] and not stats['jumping']:
        jump_time = time
        stats['jumping'] = True

    if stats['jumping']:
        delta[1] = -get_vy((time - jump_time) * 0.03)
        if rect.bottom >= height and delta[1] > 0:
            stats['jumping'] = False
            delta[1] = 0

    # Move! Move!!!
    if key_stats['a_down'] and key_stats['d_down']:
        if key_stats['d_time'] > key_stats['a_time']:
            stats['moving'] = 'right'
        else:
            stats['moving'] = 'left'
    else:
        if key_stats['a_down']:
            stats['moving'] = 'left'
        elif key_stats['d_down']:
            stats['moving'] = 'right'
        else:
            stats['moving'] = 'stand'

    if stats['moving'] == 'right':
        delta[0] = speed
        stats['forward'] = 'right'
    elif stats['moving'] == 'left':
        delta[0] = -speed
        stats['forward'] = 'left'

    rect = rect.move(delta)

    limit_in_view()

    screen.fill((100, 50, blue))
    if stats['forward'] == 'right':
        if stats['shooting']:
            screen.blit(player_shoot, rect)
        else:
            screen.blit(player, rect)
    else:
        if stats['shooting']:
            screen.blit(player_shoot_left, rect)
        else:
            screen.blit(player_left, rect)

    pygame.display.update()

    # Useless
    useless_background()

    time += 1

pygame.quit()
