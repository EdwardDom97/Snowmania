import pygame
import sys
from pygame.locals import *

pygame.init()

# Screen setup
screen_width, screen_height = 800, 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snowmania       Tristan Dombroski       itch.io  GAMEJAM #145 "Frozen"')

# Menusplash setup
menusplash = pygame.image.load('graphics/snowmaniasplash.png')
menusplash_rect = menusplash.get_rect(topleft=(0, 0))

# Start button setup
startbutton = pygame.image.load('graphics/startbuttonimage.png')
startbutton_rect = startbutton.get_rect(midleft=(250, 600))

# Clock setup
clock = pygame.time.Clock()

# Player setup
player = pygame.image.load('graphics/snowbob.png')
player_rect = player.get_rect(bottomleft=(400, 600))
player_y_speed = 0
gravity = 0.8
is_jumping = False

# Ground setup, creates a basic rectanlge 600 units/pixels wide and 50 tall
ground_rect = pygame.Rect(0, 600, screen_width, 50)

# Game state setup
game_running = True
game_state = 'MENU'

# Event handling setup
mouse_clicked = False
mouse_pos = (0, 0)

while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            mouse_clicked = True
            mouse_pos = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    if game_state == 'MENU':

        if mouse_clicked and startbutton_rect.collidepoint(mouse_pos):
            game_state = 'GAME'


    elif game_state == 'GAME':


        if keys[K_LEFT]:
            player_rect.x -= 5

        if keys[K_RIGHT]:
            player_rect.x += 5

        if keys[K_SPACE] and not is_jumping:
            player_y_speed = -15
            is_jumping = True

        if is_jumping:
            player_y_speed += gravity
            player_rect.y += player_y_speed

            if player_rect.colliderect(ground_rect):
                is_jumping = False
                player_rect.y = ground_rect.y - player_rect.height

    screen.fill((135, 212, 221))

    if game_state == 'MENU':
        screen.blit(menusplash, menusplash_rect)
        screen.blit(startbutton, startbutton_rect)


    elif game_state == 'GAME':
        screen.blit(player, player_rect)
        pygame.draw.rect(screen, (0, 255, 0), ground_rect)

    pygame.display.update()
    clock.tick(60)