#this is for the mini-jam on itch.io #145 'Frozen'
#last edit for the night, re-adding my comments and cleaning some code up

#load the pygame library
import pygame
import sys
import random
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


#before loading the player, environment, enemies, and objects, I am going to make my world variables
#going to try to make a maximum world size so it's a little easier making presents and the end goal spawn in the environment 
WORLD_WIDTH = 1000
WORLD_HEIGHT = 650
# Scrolling setup
scroll_background_x = 5
scroll_speed = 5

#start player variables code 


# Player setup including variables that will control the player during the game state. Did not want to make a class Player
#player images
player = pygame.image.load('graphics/snowbob.png')
player_rect = player.get_rect(bottomleft=(400, 600))

#player variables
player_score = 0
player_health = 100
player_lives = 3
player_y_speed = 0
player_x_speed = 3
gravity = .7
distance_travelled = 0 #this will be used as a marker to the end of the game
is_jumping = False #starting this variable off as false so I can execute a later action


# Player starting position
player_starting_position = (0, WORLD_HEIGHT - player_rect.height)

#end players code



#start healthbarcode

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
fireball_speed = 4
fireballs = []


#here I am going to add snow to the game that heals the player if the player collides with it
snowflake_image = pygame.image.load('graphics/snowflake.png')
snowflakes = []  # List to store active snowflakes on screen similar to fireballs and how I handled enemies in slime hope infinity
snowflake_speed = random.choice(range(1, 3)) #this allows for faster and slower snowflakes which adds to the game environment

#WOLF ENEMY
#here I am going to introduce an enemy to the game for the player to avoid while walking. will appear from the right at random intervals, sometimes multiple enemies.
enemy_image = pygame.image.load('graphics/badwolf.png')
enemy_x_speed = 3
enemy_y_speed = 0
enemy_health = 2
enemy_wolves = []

#BEAR ENEMY
enemy_bear_image = pygame.image.load('graphics/snowbear.png')
enemy_x_speed = 2
enemy_y_speed = 0
enemy_health = 3
enemy_bears = []


# Initialize an enemy reset timer
reset_timer = pygame.time.get_ticks()

#images to display during the game over screen


#GROUND
#here I want to reattempt making a ground setup but using snowblock.png and then a for i in something set-up
ground_surface = pygame.image.load('graphics/snowblock.png')
ground_surface_rect = ground_surface.get_rect()
ground_y = screen_height - ground_surface_rect.height


#GROUND OBJECT
#STATIONARY OBJECT LOGIC start
#here I am going to attempt a stationary object for the player top hop over
stationary_objects = [
    pygame.image.load('graphics/snowtree.png')
]

stationary_objects_rects = []

num_objects = 1  # Adjust the number of objects as needed
spawn_on_every = random.choice([1, 2])  # Randomly choose the spawn frequency

current_x = 0

for i in range(num_objects):
    if i % spawn_on_every == 0:
        obj_rect = stationary_objects[0].get_rect()
        obj_rect.x = current_x - scroll_background_x  # Subtract scroll_background_x to make it stationary
        obj_rect.y = ground_y - obj_rect.height
        obj_image = stationary_objects[0]
        stationary_objects_rects.append((obj_rect, obj_image))

    current_x += ground_surface_rect.width

#STATIONARY OBJECT LOGIC END



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
        snowflakes.clear()
        enemy_wolves.clear()

        #resetting the distance travelled, player score and health.
        distance_travelled = 0
        player_score = 0
        player_health = 100

        #resetting the game completed to false
        game_completed = False

        menu_toggled = False #creating this variable and setting it to false so when the player returns to the menu and back to the game the menu button is not displayed.


        if mouse_clicked and startbutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            #endgoal_rect = endgoal_image.get_rect(bottomleft=(-600,-600)) #this ensures that during the menu state and in betwen game sessions, the endgoal_rect is placed far off screen

            game_state = 'GAME'

    #END OF MENU LOOP LOGIC





    #START OF ACTIVE GAME LOOP LOGIC

    elif game_state == 'GAME': #the game state will handle all the game logic like player movement, event keys, enemies, objects, and their respective code sections

        
        if mouse_clicked and menubutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            game_state = 'MENU'


        #start of wolf creation logic
        #handles the creation of wolf enemies onscreen for the player to defeat/avoid
        if random.randint(0, 400) < 0.8:
            new_enemy_rect = enemy_image.get_rect(topleft=(screen_width, ground_y - enemy_image.get_height()))
            enemy_wolves.append({'rect': new_enemy_rect, 'speed': 3, 'health': 1})

        # Update position of existing enemies
        for wolf in enemy_wolves:
            wolf['rect'].x -= wolf['speed']

        #end of wolf creation logic

        #start of bear creation logic
        #handles the creation of wolf enemies onscreen for the player to defeat/avoid
        if random.randint(0, 400) < 0.8:
            bear_enemy_rect = enemy_bear_image.get_rect(topleft=(screen_width, ground_y - enemy_bear_image.get_height()))
            enemy_bears.append({'rect': bear_enemy_rect, 'speed': 2, 'health': 3})

        # Update position of existing enemies
        for bear in enemy_bears:
            bear['rect'].x -= bear['speed']

        #end of bear creation logic




        #this code sections handles player movement

        if keys[K_a]: #left

            player_rect.x -= player_x_speed

            # Limit to the right edge
            if player_rect.right > WORLD_WIDTH:
                player_rect.right = WORLD_WIDTH
   
            # Limit to the left edge
            if player_rect.left < 50:
                player_rect.left = 50  


          
        if keys[K_d]: #right

            player_rect.x += player_x_speed

            if player_rect.right > screen_width - 150:
                player_rect.right = screen_width - 150  # Limit to the right edge

            scroll_background_x += 3
            distance_travelled += 1

        if keys[K_w] and not is_jumping:
            player_y_speed = -15
            is_jumping = True
        

        #shooting logic
        if keys[K_SPACE] and can_fire: #this section handles the event spacebar being pressed and contains the necessary elements for a basic shooting function with math. (aims for mouse_pos)

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

            #if fireball_rect.colliderect(enemy_rect):
                #enemy_health -= 1

            if player_health <= 0:
                distance_travelled = 0
                player_health = 100
                game_completed = False
                game_state = 'GAMEOVER'
                
        if event.type == KEYUP and event.key == K_SPACE:
            can_fire = True
        
        #end of player movement logic and condtions
        
        #snowcode
        #here I am going to try my snow logic
        if random.randint(0, 100) < 3:  # Adjust the probability of generating a snowflake
            snowflake_rect = snowflake_image.get_rect()
            snowflake_rect.x = random.randint(0, screen_width)
            snowflake_rect.y = 0
            snowflakes.append(snowflake_rect)



        # Update snowflakes
        for snowflake_rect in snowflakes:
            snowflake_rect.y += snowflake_speed

            # Check collision with the ground
            if snowflake_rect.y >= ground_y:
                snowflakes.remove(snowflake_rect)

            # Check collision with the player
            if snowflake_rect.colliderect(player_rect):
                player_score += 1 

                if player_health <= 100:
                    player_health += 2
                    snowflakes.remove(snowflake_rect)

        #end update for snowflake code


        #this section is purely for the wolf enemy
        #wolf collision with the player
        for wolf in enemy_wolves:
            if player_rect.colliderect(wolf['rect']):
                player_health -= 10  # Decrease player health upon collision with a wolf
                enemy_wolves.remove(wolf)

            if player_health <= 0:
                distance_travelled = 0
                player_health = 100
                game_completed = False
                game_state = 'GAMEOVER'

        #wolf collision with fireballs
        for fireball_rect, direction in fireballs.copy():
            for wolf in enemy_wolves.copy():
                if wolf['rect'].colliderect(fireball_rect):
                    wolf['health'] -= 1  # Decrease wolf health upon collision with a fireball
                    
                    if wolf['health'] <= 0:
                        player_score += 3
                        enemy_wolves.remove(wolf)  # Remove the wolf if its health is depleted

                    fireballs.remove((fireball_rect, direction))  # Remove the fireball upon collision
                                

        #end of wolf code logic



        #here I am going to attempt to add a function that keeps the player's health at a certain max value (logic)
        if player_health >= 100:
            player_health = 100


        # Update player's vertical position
        player_rect.y += player_y_speed


        # Check for collision with the ground
        if player_rect.bottom >= ground_y:
            is_jumping = False
            player_rect.y = ground_y - player_rect.height


        # Apply gravity
        player_y_speed += gravity


        #puts the endgoal_rect on screen if the victory condition is met
        #if distance_travelled >= WORLD_WIDTH and not game_completed:
        #    endgoal_rect.bottomleft = (WORLD_WIDTH - scroll_background_x + 460, 590)


        


        #END OF ACTIVE GAME LOOP LOGIC




        #START OF GAME OVER LOOP LOGIC


    elif game_state == 'GAMEOVER':


        #including some variables right here to make the game reset better like distance travelled and player health
        #resetting the enemy position
        #enemy_rect.x = screen_width + 1000
        #resetting the player health and position
        player_health = 100
        player_rect = player.get_rect(bottomleft=(400, 600))
        #resetting the distance travelled
        distance_travelled = 0


        if mouse_clicked and menubutton_rect.collidepoint(mouse_pos): #allows the player to start the game
            #endgoal_rect = endgoal_image.get_rect(bottomleft=(-600,-600)) #this ensures that during the menu state and in betwen game sessions, the endgoal_rect is placed far off screen

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
            x_position = (i * ground_surface_rect.width) - scroll_background_x % ground_surface_rect.width
            screen.blit(ground_surface, (x_position, ground_y))

            # Drawing ground obstacles with the ground loop
            if i % spawn_on_every == 0:
                for obj_rect, obj_image in stationary_objects_rects:
                    stationary_object_x_position = (
                        i * ground_surface_rect.width
                    ) - scroll_background_x % ground_surface_rect.width + obj_rect.x
                    screen.blit(
                        obj_image,
                        (stationary_object_x_position, ground_y - obj_rect.height),
                    )
            #END OF GROUND STATIONARYOBJECT RENDERING

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

        # Inside the 'GAME' loop, after updating the player's score
        score_text = game_font.render("Score: {}".format(player_score), True, (255, 255, 255))
        screen.blit(score_text, (10, 50))  # Adjust the position as needed

    
        #healthbar Draw the green health bar on top of the base health bar
        screen.blit(playerhealth_visual, playerhealth_visual_rect)
        pygame.draw.rect(screen,  current_healthbar_color,  current_healthbar_rect)


        #first enemy wolf
        for wolf in enemy_wolves:
            screen.blit(enemy_image, wolf['rect'].topleft)

        #second enemy bear
        for bear in enemy_bears:
            screen.blit(enemy_bear_image, bear['rect'].topleft)


        #player
        screen.blit(player, player_rect) 
        #pygame.draw.rect(screen, (0, 255, 0), ground_rect)


        #shooting
        for fireball_rect, direction in fireballs: #this is what updates the RENDERING of the fireball attacks the list of fireballs more namely.
            fireball_rect.x += direction[0] * fireball_speed
            fireball_rect.y += direction[1] * fireball_speed

            #render the fireball
            screen.blit(fireball_image, fireball_rect)


        #snow
        # Rendering snowflakes
        for snowflake_rect in snowflakes:
            screen.blit(snowflake_image, snowflake_rect)


        #presents
        #for present_rect in presents:
            #screen.blit(present_image, present_rect)

    #END OF GAME ACTIVE LOOP RENDERING




    #START OF GAMEOVER LOOP RENDERING

    elif game_state == 'GAMEOVER':


        #game_completed = False
        distance_travelled = 0               
        screen.fill((135, 212, 221))
        screen.blit(gameover_image, gameover_image_rect)
        screen.blit(menubutton, menubutton_rect)


        #if the game was completed will display a different screen, 'you win' screen
        if game_completed:
            distance_travelled = 0
            screen.fill((135, 212, 221))
            screen.blit(game_completed_image, game_completed_image_rect)
            screen.blit(menubutton, menubutton_rect)

            

    pygame.display.update() #updates the screen during the game
    clock.tick(60) #clocks the game to 60 frames per second