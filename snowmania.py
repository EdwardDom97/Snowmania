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
player_x_speed = 3
gravity = .7
is_jumping = False

# Ground setup, creates a basic rectanlge 600 units/pixels wide and 50 tall
#ground_rect = pygame.Rect(0, 600, screen_width, 50)

#here I want to reattempt making a ground setup but using snowblock.png and then a for i in something set-up
ground_surface = pygame.image.load('graphics/snowblock.png')
ground_surface_rect = ground_surface.get_rect()
ground_y = screen_height - ground_surface_rect.height

# Scrolling setup
scroll_x = -50


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


        if keys[K_a]: #left

            player_rect.x -= player_x_speed
            if player_rect.left < 50:
                player_rect.left = 50  # Limit to the left edge

            #scroll_x -= 5


        if keys[K_d]: #right

            player_rect.x += player_x_speed
            if player_rect.right > screen_width - 150:
                player_rect.right = screen_width - 150  # Limit to the right edge

            scroll_x += 4

        if keys[K_w] and not is_jumping:
            player_y_speed = -15
            is_jumping = True

        # Update player's vertical position
        player_rect.y += player_y_speed

        # Check for collision with the ground
        if player_rect.bottom >= ground_y:
            is_jumping = False
            player_rect.y = ground_y - player_rect.height

        # Apply gravity
        player_y_speed += gravity

    screen.fill((135, 212, 221))



    if game_state == 'MENU':
        screen.blit(menusplash, menusplash_rect)
        screen.blit(startbutton, startbutton_rect)


    elif game_state == 'GAME':
        # Draw the ground surface in a loop
        for i in range(-5, (screen_width // ground_surface_rect.width) + 5):
            x_position = (i * ground_surface_rect.width) - scroll_x % ground_surface_rect.width
            screen.blit(ground_surface, (x_position, ground_y))


        screen.blit(player, player_rect)
        #pygame.draw.rect(screen, (0, 255, 0), ground_rect)


    elif game_state == 'GAMEOVER':
        screen.fill((135, 212, 221))

    pygame.display.update()
    clock.tick(60)