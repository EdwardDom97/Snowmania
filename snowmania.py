#this is for the mini-jam on itch.io #145 'Frozen'
#last edit for the night, re-adding my comments and cleaning some code up

#load the pygame library
import pygame
import sys
from pygame.locals import *

#being with initializing the program
pygame.init()

#caption for gamejam game snowmania
pygame.display.set_caption('Snowmania       Tristan Dombroski       itch.io  GAMEJAM #145 "Frozen"') #this sets a caption for the application itself


# Screen setup
screen_width, screen_height = 800, 650
screen = pygame.display.set_mode((screen_width, screen_height))
#captioning the window
pygame.display.set_caption('Snowmania       Tristan Dombroski       itch.io  GAMEJAM #145 "Frozen"')

# Menusplash setup
menusplash = pygame.image.load('graphics/snowmaniasplash.png')
menusplash_rect = menusplash.get_rect(topleft=(0, 0))

# Start button setup
startbutton = pygame.image.load('graphics/startbuttonimage.png')
startbutton_rect = startbutton.get_rect(midleft=(250, 600))

# Clock setup
clock = pygame.time.Clock()

# Player setup including variables that will control the player during the game state. Did not want to make a class Player
player = pygame.image.load('graphics/snowbob.png')
player_rect = player.get_rect(bottomleft=(400, 600))
player_y_speed = 0
player_x_speed = 3
gravity = .7
is_jumping = False #starting this variable off as false so I can execute a later action



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

#the main game loop itself
while game_running:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            mouse_clicked = True
            mouse_pos = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed() #this variable set to the event key get pressed checks for any and all keys pressed on the keyboard during the runtime of this program

    if game_state == 'MENU': #the menu will display options and buttons like sounds, or start game, or maybe highscore

        if mouse_clicked and startbutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            game_state = 'GAME'



    elif game_state == 'GAME': #the game state will handle all the game logic like player movement, event keys, enemies, objects, and their respective code sections


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

    screen.fill((135, 212, 221)) #fills the screen with an arctic sky color



    if game_state == 'MENU': #draws my menu
        screen.blit(menusplash, menusplash_rect)
        screen.blit(startbutton, startbutton_rect)


    elif game_state == 'GAME': #draws the game player, objects, enemies, and environment
        # Draw the ground surface in a loop
        for i in range(-5, (screen_width // ground_surface_rect.width) + 5):
            x_position = (i * ground_surface_rect.width) - scroll_x % ground_surface_rect.width
            screen.blit(ground_surface, (x_position, ground_y))


        screen.blit(player, player_rect)
        #pygame.draw.rect(screen, (0, 255, 0), ground_rect)


    elif game_state == 'GAMEOVER': #this is if the player dies
        screen.fill((135, 212, 221))

    pygame.display.update() #updates the screen during the game
    clock.tick(60) #clocks the game to 60 frames per second