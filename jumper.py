import pygame
import sys
from pygame.locals import *

pygame.init()

WINDOW_SIZE = (800, 650)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

player_rect = pygame.Rect(100, 100, 30, 30)
player_y_speed = 0
gravity = 0.8
is_jumping = False

ground_rect = pygame.Rect(0, 600, WINDOW_SIZE[0], 50)

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and not is_jumping:
                player_y_speed = -15
                is_jumping = True

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_rect.x -= 5
    if keys[K_RIGHT]:
        player_rect.x += 5

    if is_jumping:
        player_y_speed += gravity
    else:
        player_y_speed = 0

    player_rect.y += player_y_speed

    if player_rect.colliderect(ground_rect):
        is_jumping = False
        player_rect.y = ground_rect.y - player_rect.height

    screen.fill((135, 212, 221))
    pygame.draw.rect(screen, (0, 255, 0), ground_rect)
    pygame.draw.rect(screen, (255, 0, 0), player_rect)

    pygame.display.update()
    clock.tick(60)