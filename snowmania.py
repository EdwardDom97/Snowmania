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
screen_height, screen_width = 800, 450 #basic screen
screen = pygame.display.set_mode((screen_height, screen_width))

#clock variable to keep frames or time going in the game
clock = pygame.time.Clock()

#menusplash
menusplash = pygame.image.load('graphics/snowmaniasplash.png')
#menubackground color is hexcode 87d4dd and I like it
menusplash_rect = menusplash.get_rect(topleft=(0, 0))


game_running = True



while True:


    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False
 
    if game_running:



        #screen.fill(0,0,0)

        screen.blit(menusplash, menusplash_rect)



    pygame.display.update()
    clock.tick(60)
    


#pygame.quit()
sys.exit() 