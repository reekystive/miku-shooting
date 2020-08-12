import pygame
from pygame import *
from time import sleep
from random import random

pygame.init()
pygame.display.set_caption("Miku Shooting")

width, height = 960, 540
player_height = 128
player_width = 106
bullet_det_height = 80
bullet_width = 48
bullet_height = 32
rabbit_height = 96
rabbit_width = 96
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))

base_loc = './resources/'
player = pygame.image.load(base_loc + "stand.png")
player_left = pygame.image.load(base_loc + "stand_left.png")
player_shoot = pygame.image.load(base_loc + "shoot.png")
player_shoot_left = pygame.image.load(base_loc + "shoot_left.png")
bg = pygame.image.load(base_loc + "background.png")
bg_cloud = pygame.image.load(base_loc + "background_cloud.png")
bullet = pygame.image.load(base_loc + "heart.png")
rabbit = pygame.image.load(base_loc + "rabbit_1.png")
rabbit_left = pygame.image.load(base_loc + "rabbit_1_left.png")

rect = player.get_rect()
rect.bottom = height
rect.left = 0

delta = [0, 0]
speed = 5.0
gravity = 8.0
jump_speed = 7.0
bullet_speed = 10.0
bullet_cd_time = 10
rabbit_speed = 10.0

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

bullets = []
rabbits = []

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

def limit_rect():
    global rect
    if rect.left < 0:
        rect.left = 0
    if rect.right > width:
        rect.right = width
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > height:
        rect.bottom = height

def limit_pos():
    global stats
    if stats['pos_x'] < -(1.5*width - player_width/2):
        stats['pos_x'] = -(1.5*width - player_width/2)
    if stats['pos_x'] > (1.5*width - player_width/2):
        stats['pos_x'] = (1.5*width - player_width/2)

def generate_bullet():
    y = stats['pos_y'] + bullet_det_height - bullet_height/2
    x = stats['pos_x']
    if stats['forward'] == 'left':
        x -= player_width/2 + bullet_width/2 - 24
    else:
        x += player_width/2 + bullet_width/2 - 24
    bullets.append({'pos': [x, y], 'direction': stats['forward'], 'relative_speed': delta})

def move_bullets():
    for bu in bullets:
        if bu['direction'] == 'left':
            bu['pos'][0] = bu['pos'][0] - bullet_speed + bu['relative_speed'][0]
        else:
            bu['pos'][0] = bu['pos'][0] + bullet_speed + bu['relative_speed'][0]
        bu['pos'][1] += bu['relative_speed'][1]

def clear_bullets():
    for i in range(len(bullets) - 1, -1, -1):
        if bullets[i]['pos'][0] + bullet_width/2 < -1.5*width \
           or bullets[i]['pos'][0] - bullet_width/2 > 1.5*width \
           or bullets[i]['pos'][1] + bullet_height < 0 \
           or bullets[i]['pos'][1] > height:
            del bullets[i]

def generate_rabbit(time):
    if random() < 0.01:
        rabbits.append({'pos': [-1.5*width - rabbit_width/2, 0], 'direction': 'right'})
    if random() < 0.01:
        rabbits.append({'pos': [1.5*width + rabbit_width/2, 0], 'direction': 'left'})

def move_rabbits():
    for rab in rabbits:
        if rab['direction'] == 'left':
            rab['pos'][0] -= rabbit_speed
        else:
            rab['pos'][0] += rabbit_speed

def clear_rabbits():
    for i in range(len(rabbits) - 1, -1, -1):
        x = rabbits[i]['pos'][0]
        if x < -1.5*width - rabbit_width/2 or x > 1.5*width + rabbit_width/2:
            del rabbits[i]

running = True
time = 0
jump_time = 0
cur_view_left = -width/2
bullet_remain_cd_time = 0

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

    # Shoot! Shoot!!!
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

    limit_pos()

    if stats['pos_x'] - player_width/2 - 64 < cur_view_left:
        cur_view_left = stats['pos_x'] - player_width/2 - 64
    if cur_view_left < -width*1.5:
        cur_view_left = -width*1.5
    if stats['pos_x'] + player_width/2 + 64 > cur_view_left + width:
        cur_view_left = stats['pos_x'] + player_width/2 + 64 - width
    if cur_view_left > width*0.5:
        cur_view_left = width*0.5

    rect.left = int(stats['pos_x'] - player_width/2 - cur_view_left)
    rect.bottom = int(height - stats['pos_y'])
    limit_rect()

    screen.blit(bg, (-cur_view_left - width/2, 0))
    screen.blit(bg, (-cur_view_left - width/2 - width, 0))
    screen.blit(bg, (-cur_view_left - width/2 + width, 0))

    pos_cloud = int(time / 5)
    screen.blit(bg_cloud, ((pos_cloud - cur_view_left) % width , 0))
    screen.blit(bg_cloud, ((pos_cloud - cur_view_left) % width - width, 0))

    # Rabbits!
    generate_rabbit(time)
    move_rabbits()
    clear_rabbits()

    for rab in rabbits:
        if rab['direction'] == 'right':
            screen.blit(rabbit, [rab['pos'][0] - rabbit_width/2 - cur_view_left, height - (rab['pos'][1] + rabbit_height)])
        else:
            screen.blit(rabbit_left, [rab['pos'][0] - rabbit_width/2 - cur_view_left, height - (rab['pos'][1] + rabbit_height)])

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

    # Shooting! Bullet!!
    if bullet_remain_cd_time == 0 and stats['shooting']:
        generate_bullet()
        bullet_remain_cd_time = bullet_cd_time

    if bullet_remain_cd_time > 0:
        bullet_remain_cd_time -= 1

    move_bullets()
    clear_bullets()

    for bu in bullets:
        screen.blit(bullet, [bu['pos'][0] - bullet_width/2 - cur_view_left, height - (bu['pos'][1] + bullet_height)])

    pygame.display.update()

    sleep(0.002)

    time += 1
    # print(stats['pos_x'])
    # print(cur_view_left)
    # print(len(bullets))
    # print(len(rabbits))

pygame.quit()
