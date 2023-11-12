#this is for the mini-jam on itch.io #145 'Frozen'
#last edit for the night, re-adding my comments and cleaning some code up

#load the pygame library
import pygame
import sys
import random
import time
import math
from pygame import font
from pygame.locals import *

#being with initializing the program
pygame.init()

#caption for gamejam game snowmania
pygame.display.set_caption('Snowmania       Tristan Dombroski       itch.io  GAMEJAM #145 "Frozen"') #this sets a caption for the application itself


# Screen setup
screen_width, screen_height = 800, 650
screen = pygame.display.set_mode((screen_width, screen_height))


# Menusplash setup
menusplash = pygame.image.load('graphics/snowmaniasplash.png')
menusplash_rect = menusplash.get_rect(topleft=(0, 0))

# Start button setup
startbutton = pygame.image.load('graphics/startbuttonimage.png')
startbutton_rect = startbutton.get_rect(midleft=(250, 600))


#setting up a menu button for the game state when the player presses escape it brings up the menu button. going to use a toggle feature similar to my crafting/help window in TribalSandbox
menubutton = pygame.image.load('graphics/menubuttonimage.png')
menubutton_rect = menubutton.get_rect(midleft=(250, 300))


# Clock setup
clock = pygame.time.Clock()

# Player setup including variables that will control the player during the game state. Did not want to make a class Player
#player images
player = pygame.image.load('graphics/snowbob.png')
player_rect = player.get_rect(bottomleft=(400, 600))
#player variables
player_health = 100
player_lives = 3
player_y_speed = 0
player_x_speed = 3
gravity = .7
distance_travelled = 0 #this will be used as a marker to the end of the game
is_jumping = False #starting this variable off as false so I can execute a later action

#here I am going to load some images related to the player like a health bar and special power icons
playerhealth_visual = pygame.image.load('graphics/snowbobhealthbar.png')
playerhealth_visual_rect = playerhealth_visual.get_rect(topleft=(50,150))

#here I am going to create a green-ish rectangle that will display ontop of playerhealth_visual_rect = playerhealth_visual.get_rect(topleft=(50,150)) equal to the player's health defined above
current_healthbar_width = 187
current_healthbar_height = 57
current_healthbar_color = (15, 225, 87)
current_healthbar_rect = pygame.Rect(playerhealth_visual_rect.x + 65, playerhealth_visual_rect.y + 5, current_healthbar_width, current_healthbar_height)


#end health bar code

#shooting
# Projectile setup
fireball_image = pygame.image.load('graphics/fireball.png')
fireball_rect = None
#fireball_rect = fireball_image.get_rect()

# Additional variable for firing cooldown
can_fire = True
fireball_damage = 1
fireball_speed = 5
fireballs = []



#here I am going to introduce an enemy to the game for the player to avoid while walking. will appear from the right at random intervals, sometimes multiple enemies.
enemy_image = pygame.image.load('graphics/badwolf.png')
enemy_image_rect = enemy_image.get_rect(topleft=(screen_width - enemy_image.get_width(), 540))
enemy_x_speed = 4
enemy_y_speed = 0
enemy_health = 2
enemy_wolves = []

# Initialize an enemy reset timer
enemy_reset_timer = pygame.time.get_ticks()

#here I want to reattempt making a ground setup but using snowblock.png and then a for i in something set-up
ground_surface = pygame.image.load('graphics/snowblock.png')
ground_surface_rect = ground_surface.get_rect()
ground_y = screen_height - ground_surface_rect.height


#adding in the endgoal image to establish a better start and stop of the game.
endgoal_image = pygame.image.load('graphics/endgoal.png')
#trying to blit the endgoal on top of the ground after a 1000 units have been travelled. starts off, off screen.
endgoal_image_rect = endgoal_image.get_rect(bottomleft=(-100, 590))


#images to display during the game over screen

#if the player died
gameover_image = pygame.image.load('graphics/gameover.png')
gameover_image_rect = gameover_image.get_rect(topleft=(0, 0))

#if the player collided with the end goal
game_completed_image = pygame.image.load('graphics/gamecompleted.png')
game_completed_image_rect = game_completed_image.get_rect(topleft=(0, 0))

#variable to control what screen displays during the end game state
game_completed = False

#game font for visual displays like score and distance
game_font = font.Font(None, 36)



# Scrolling setup
scroll_x = 0

# Game state setup
game_running = True
game_state = 'MENU'

# Event handling setup
mouse_clicked = False
mouse_pos = (0, 0)
menu_toggled = False #this is the state/variable that controls the display of the menu button



#the main game loop itself
while game_running:

    #tracks time
    current_time = pygame.time.get_ticks()
    #tracks players distance traveled

    #I want to try to track the spell cast time

    
    #distance_travelled = 0 #this will be used as a marker to the end of the game

    #keys
    
    keys = pygame.key.get_pressed() #this variable set to the event key get pressed checks for any and all keys pressed on the keyboard during the runtime of this program


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            mouse_clicked = True
            mouse_pos = pygame.mouse.get_pos()

        elif event.type == KEYUP:
            if keys[K_ESCAPE]:
                menu_toggled = not menu_toggled


    #the codes, functions and variables above effect the rest of the code below in the respective active loops. time, keys, and if the system quits.



    #START OF MENU LOGIC

    if game_state == 'MENU': #the menu will display options and buttons like sounds, or start game, or maybe highscore
        #clearing the fireball list inside of the menu so when a new game is started from previously dying, no fireballs remain on screen
        fireballs.clear()
        #resetting the distance travelled
        distance_travelled = 0
        #setting the endgoal_image_rect off screen
        endgoal_image_rect = endgoal_image.get_rect(bottomleft=(-100, 590))
        #resetting the game completed to false
        game_completed = False

        menu_toggled = False #creating this variable and setting it to false so when the player returns to the menu and back to the game the menu button is not displayed.


        if mouse_clicked and startbutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            game_state = 'GAME'

    #END OF MENU LOOP LOGIC





    #START OF ACTIVE GAME LOOP LOGIC

    elif game_state == 'GAME': #the game state will handle all the game logic like player movement, event keys, enemies, objects, and their respective code sections

        

        if mouse_clicked and menubutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            game_state = 'MENU'

        #this code sections handles player movement

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
            distance_travelled += 1

        if keys[K_w] and not is_jumping:
            player_y_speed = -15
            is_jumping = True
        

        if keys[K_SPACE] and can_fire:

            #fireballs = []

            player_health -= 15

            current_time = pygame.time.get_ticks()


            fireball_rect = fireball_image.get_rect()
            fireball_rect.center = player_rect.center

            #grabs the current position of the mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate the direction from player to mouse
            direction_x = mouse_x - fireball_rect.centerx
            direction_y = mouse_y - fireball_rect.centery

            # Normalize the direction vector #thanks to chat gpt honestly, I dont know the logic behind this
            magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
            direction = (direction_x / magnitude, direction_y / magnitude)
                  
                    
            # Adjust the position and speed based on the direction
            fireball_rect.x += direction[0] * fireball_speed
            fireball_rect.y += direction[1] * fireball_speed

            fireballs.append((fireball_rect, direction))

            # Remove fireballs that go off-screen
            fireballs = [(rect, direction) for rect, direction in fireballs if screen.get_rect().colliderect(rect)]

            fireball_cooldown = current_time

            can_fire = False

            if fireball_rect.colliderect(enemy_image_rect):
                enemy_health -= 1

            if player_health <= 0:
                distance_travelled = 0
                player_health = 100
                game_completed = False
                game_state = 'GAMEOVER'
                
        if event.type == KEYUP and event.key == K_SPACE:
            can_fire = True
        
        

            #additional logic like enemy collision

        #end shooting

        #this section is purely for the wolf enemy

        # Update the enemy's position from right to left
        enemy_image_rect.x -= enemy_x_speed


        # Reset enemy position when it goes off the left side of the screen and includes a timer so the player is not hopping for dear life every three seconds
        if enemy_image_rect.right <= -1000 and current_time - enemy_reset_timer > random.randint(8000, 12000):
            enemy_image_rect.x = screen_width + 1000
            enemy_image_rect.y = 540
            enemy_reset_timer = current_time
            

        # Check for collision beteen the player and the wolf enemy
        if player_rect.colliderect(enemy_image_rect):
            # Handle collision (e.g., decrease player health)
            player_health -= 10  # Adjust the amount based on your game's balancing
            if player_health <= 0:
                
                distance_travelled = 0
                player_health = 100
                game_completed = False
                game_state = 'GAMEOVER'


        #handles collision between the fireballs and the enemies
        for fireball_rect, direction in fireballs:
            if fireball_rect.colliderect(enemy_image_rect):
                enemy_health -= 1
                fireballs.remove((fireball_rect, direction))  # Remove the fireball when it hits the enemy

                # Check if the enemy is defeated
                if enemy_health <= 0:
                    # Reset enemy position
                    enemy_image_rect.x = screen_width + 1000
                    # Reset enemy health
                    enemy_health = 2


        #handles collision between the player and the end goal
        if player_rect.colliderect(endgoal_image_rect):
            #moving the endgoal_image_rect off screen for the next iteration of the gameplay
            endgoal_image_rect = endgoal_image.get_rect(bottomleft=(-100, 590))
            #resetting distance travelled
            distance_travelled = 0
            player_health = 100
            game_completed = True
            game_state = 'GAMEOVER'
            


        # Update player's vertical position
        player_rect.y += player_y_speed


        # Check for collision with the ground
        if player_rect.bottom >= ground_y:
            is_jumping = False
            player_rect.y = ground_y - player_rect.height

        # Apply gravity
        player_y_speed += gravity


        if distance_travelled >= 500 and not game_completed:
            endgoal_image_rect.bottomleft = (460, 590)


        #END OF ACTIVE GAME LOOP LOGIC





        #START OF GAME OVER LOOP LOGIC


    elif game_state == 'GAMEOVER':


        #including some variables right here to make the game reset better like distance travelled and player health
        #resetting the enemy position
        enemy_image_rect.x = screen_width + 1000
        #resetting the player health and position
        player_health = 100
        player_rect = player.get_rect(bottomleft=(400, 600))
        #resetting the distance travelled
        distance_travelled = 0


        if mouse_clicked and menubutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            game_state = 'MENU'

        

        


        #END OF THE GAME OVER LOOP LOGIC
    



    #the code above this comment handles the logical events like key presses and clicks, also checks for other conditionals like object/envrionmental collisions




    # RENDERING IN THE GAMES STATES ARE BELOW WHILE LOGIC IN THE GAME STATES ARE ABOVE




    #the code below this comment handles displaying everything onto the screen during the proper game_states




    screen.fill((135, 212, 221)) #fills the screen with an arctic sky color



    #START OF THE MENU RENDERING

    if game_state == 'MENU': #draws my menu
        screen.blit(menusplash, menusplash_rect)
        screen.blit(startbutton, startbutton_rect)


    #END OF THE MENU RENDERING


    #START OF GAME LOOP RENDERING

    elif game_state == 'GAME': #draws the game player, objects, enemies, and environment


        # Draw the ground surface in a loop
        for i in range(-5, (screen_width // ground_surface_rect.width) + 5):
            x_position = (i * ground_surface_rect.width) - scroll_x % ground_surface_rect.width
            screen.blit(ground_surface, (x_position, ground_y))

        #blitting the endgoal
        if distance_travelled >= 500 and not game_completed: #500 for now for easy testing
            screen.blit(endgoal_image, endgoal_image_rect)

        #going to see if I need to display the menu button here and a conditional loop to show it when escape is pressed.
        if menu_toggled:
            screen.blit(menubutton, menubutton_rect)


        #here I am going to display/blit the player image onto the screen and then other related objects and needed visuals (enemies, objects, health, powers)
        
        # Update the green health bar width based on the player's health
        current_healthbar_rect.width = int((player_health / 100) * current_healthbar_width)

        #the distance the player is travelling visually represented
        distance_text = game_font.render("Distance: {}".format(distance_travelled), True, (255, 255, 255))

        #distance the player has travelled displayed onto the screen
        screen.blit(distance_text, (10, 10))

    

        #healthbar Draw the green health bar on top of the base health bar
        screen.blit(playerhealth_visual, playerhealth_visual_rect)
        pygame.draw.rect(screen,  current_healthbar_color,  current_healthbar_rect)


        #first enemy wolf
        screen.blit(enemy_image, enemy_image_rect)

        #player
        screen.blit(player, player_rect) 
        #pygame.draw.rect(screen, (0, 255, 0), ground_rect)


        #shooting
        for fireball_rect, direction in fireballs: #this is what updates the RENDERING of the fireball attacks the list of fireballs more namely.
            fireball_rect.x += direction[0] * fireball_speed
            fireball_rect.y += direction[1] * fireball_speed

            #render the fireball
            screen.blit(fireball_image, fireball_rect)



    #END OF GAME ACTIVE LOOP RENDERING



    #START OF GAMEOVER LOOP RENDERING

    elif game_state == 'GAMEOVER':
                       
        screen.fill((135, 212, 221))
        screen.blit(gameover_image, gameover_image_rect)
        screen.blit(menubutton, menubutton_rect)


        #if the game was completed will display a different screen, 'you win' screen
        if game_completed:
        
            screen.fill((135, 212, 221))
            screen.blit(game_completed_image, game_completed_image_rect)
            screen.blit(menubutton, menubutton_rect)




    pygame.display.update() #updates the screen during the game
    clock.tick(60) #clocks the game to 60 frames per second