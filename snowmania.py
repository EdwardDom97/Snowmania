#this is for the mini-jam on itch.io #145 'Frozen'

#start by loading in my modules/libraries/stuff
import pygame
import sys
from pygame.locals import *


#this pygame.init basically initiallizes pygame

pygame.init()

#caption for gamejam game snowmania
pygame.display.set_caption('Snowmania       Tristan Dombroski       itch.io  GAMEJAM #145 "Frozen"') #this sets a caption for the application itself


#this is going to be my screen or window variable
screen_width, screen_height = 800, 650 #basic screen
screen = pygame.display.set_mode((screen_width, screen_height))

#clock variable to keep frames or time going in the game
clock = pygame.time.Clock()

#menusplash
#menubackground color is hexcode 87d4dd or rgb (135, 212, 221) and I like it
menusplash = pygame.image.load('graphics/snowmaniasplash.png')
menusplash_rect = menusplash.get_rect(topleft=(0, 0))

#start button to click and start the game, or swap to a game state
startbutton = pygame.image.load('graphics/startbuttonimage.png')
startbutton_rect = startbutton.get_rect(midleft=(250, 600))


#ground
#here I am going to load my environment images like the topblock (snowblock.png) and the underlying tiles/blocks (dirtblock.png) in a row/column fashion
topground = pygame.image.load('graphics/snowblock.png')
num_tiles = screen_width // topground.get_width()


#below loading my player I am going to create additional variables for the player regarding the game state
# Player setup
player = pygame.image.load('graphics/snowbob.png')
player_rect = player.get_rect(topleft=(400, 400))
player_y_speed = 0
gravity = 0.8
is_jumping = False

#variable to make game run or not run and setting the starting value to menu 
game_running = True
game_state = 'MENU'

#certain variables to handle logic below like mouseclicks.
mouse_clicked = False
mouse_pos = (0, 0)

#attempting to create three separate states to have a menu screen, and active game state, and a game over state.
game_menu = 'MENU'

game_active = 'GAME'

game_over = 'GAMEOVER'


#here I am creating a class called define events 
def handle_events():
    global mouse_clicked, mouse_pos, game_state, player_y_speed, player_x_speed

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_clicked = True
            mouse_pos = pygame.mouse.get_pos()

            if startbutton_rect.collidepoint(mouse_pos):
                game_state = 'GAME'
   

    keys = pygame.key.get_pressed()


    if keys[K_a]:
        player_rect.x -= 5
    if keys[K_d]:
        player_rect.x += 5
        keys = pygame.key.get_pressed()

    if keys[K_w]and not is_jumping:
        player_y_speed = -15
        is_jumping = True
        

    player_rect.y += player_y_speed


def draw_menu():
    screen.blit(menusplash, menusplash_rect)
    screen.blit(startbutton, startbutton_rect)






def draw_game():
    global player_y_speed, player_x_speed, is_jumping

    screen.fill((135, 212, 221))

    # Create a new rect for the player's position
    
    for i in range(num_tiles + 1):
        topground_rect = pygame.Rect(i * topground.get_width(), screen_height - topground.get_height(), topground.get_width(), topground.get_height())
        screen.blit(topground, topground_rect)


    if player_rect.colliderect(topground_rect):
        is_jumping = False
        player_rect.y = topground_rect.y - player_rect.height


    # Draw player
    screen.blit(player, player_rect)

    pygame.display.update()





def draw_game_over():
    screen.fill((135, 212, 221))






while game_running:

    handle_events()


    if game_state == 'MENU':
        draw_menu()


    elif game_state == 'GAME':
        draw_game()


    elif game_state == 'GAMEOVER':
        draw_game_over()


    pygame.display.update()

    clock.tick(60)