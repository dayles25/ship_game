import pygame
from time import sleep
from background import grid, TILE_SIZE, draw_background
import sys
from ship import Ship
from sunk_ship import SunkShip
import math

# init pygame
pygame.init()
clock = pygame.time.Clock()

# define grid
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE

#draw screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


ship = Ship(screen)
sunk_ship = SunkShip(screen)
bg = draw_background((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont(None, 24)
score = 1024

# while loop that runs the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            if event.key == pygame.K_UP:
                ship.change_speed(1)
            if event.key == pygame.K_DOWN:
                ship.change_speed(-1)
            if event.key == pygame.K_RIGHT:
                ship.change_omega(1)
            if event.key == pygame.K_LEFT:
                ship.change_omega(-1)

    #use clock to slow down fps

    pygame.display.set_caption(f"Ships Ahoy {clock.get_fps():.0f}")
    screen.blit(bg, bg.get_rect())
    sunk_ship.draw()
    ship.update()
    ship.draw()

    #add score
    #img = font.render(f"Score: {score}", True, (255, 0, 0))

    pygame.display.flip()

    clock.tick(60)