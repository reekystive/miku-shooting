import pygame
from pygame import *
from time import sleep

pygame.init()

width, height = 960, 540
player_height = 128
player_width = 106
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))

base_loc = './resources/'
player = pygame.image.load(base_loc + "stand.png")
player_left = pygame.image.load(base_loc + "stand_left.png")
player_shoot = pygame.image.load(base_loc + "shoot.png")
player_shoot_left = pygame.image.load(base_loc + "shoot_left.png")
bg = pygame.image.load(base_loc + "background.png")
bg_cloud = pygame.image.load(base_loc + "background_cloud.png")

rect = player.get_rect()
rect.bottom = height
rect.left = 0

delta = [0, 0]
speed = 5.0
gravity = 8.0
jump_speed = 5.0

key_stats = {'w_down': False,
             'a_down': False,
             'd_down': False,
             'a_time': -1,
             'd_time': -1,
             'j_down': False}

stats = {'moving': 'stand',
         'forward': 'right',
         'shooting': False,
          'jumping': False,
          'pos_x': 0.0,
          'pos_y': 0.0}

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
    global stats
    if stats['pos_x'] < -(1.5*width - player_width / 2):
        stats['pos_x'] = -(1.5*width - player_width / 2)
    if stats['pos_x'] > (1.5*width - player_width / 2):
        stats['pos_x'] = (1.5*width - player_width / 2)
    if rect.left < 0:
        rect.left = 0
    if rect.right > width:
        rect.right = width
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > height:
        rect.bottom = height

running = True
time = 0
jump_time = 0
cur_view_left = 0

while running:
    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
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
        delta[1] = get_vy((time - jump_time) * 0.03)
        if rect.bottom >= height and delta[1] < 0:
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

    stats['pos_x'] += delta[0]
    stats['pos_y'] += delta[1]

    if stats['pos_x'] + width / 2 - player_width / 2 - 32 < cur_view_left:
        cur_view_left = stats['pos_x'] + width / 2 - player_width / 2 - 32
    if cur_view_left < -width:
        cur_view_left = -width
    if stats['pos_x'] + width / 2 + player_width / 2 + 32 > cur_view_left + width:
        cur_view_left = stats['pos_x'] + width / 2 + player_width / 2 + 32 - width
    if cur_view_left > width:
        cur_view_left = width

    rect.left = int(stats['pos_x'] + width / 2 - player_width / 2 - cur_view_left)
    rect.bottom = int(height - stats['pos_y'])

    limit_in_view()

    screen.blit(bg, (-cur_view_left, 0))
    screen.blit(bg, (-cur_view_left - width, 0))
    screen.blit(bg, (-cur_view_left + width, 0))

    pos_cloud = int((time / 5) % width)
    screen.blit(bg_cloud, (pos_cloud, 0))
    screen.blit(bg_cloud, (pos_cloud - width, 0))

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

    sleep(0.002)

    time += 1
    # print(stats['pos_x'])
    # print(cur_view_left)

pygame.quit()
