import pygame
from time import sleep
from background import grid, TILE_SIZE, draw_background
import sys
from ship import Ship
from sunk_ship import SunkShip
import math
from wall import Wall

# init pygame
pygame.init()
clock = pygame.time.Clock()

# define grid
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE

#draw screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


ship = Ship()
sunk_ship = SunkShip(screen)
wall_1 = Wall((0,0))

wall_group = pygame.sprite.Group()
wall_group.add(wall_1)

for x in range(0, WINDOW_WIDTH, TILE_SIZE):
    for y in (0, WINDOW_HEIGHT+64):
        wall = Wall((x, y))
        wall_group.add(wall)

for y in range(0, WINDOW_WIDTH, TILE_SIZE):
    for x in (0, WINDOW_HEIGHT+192):
        wall = Wall((x, y))
        wall_group.add(wall)


bg = draw_background((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont(None, 24)
score = 1024


def _check_events(self):
    '''respond to keypress and mouse events'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            self._check_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self._check_keyup_events(event)


def _check_keydown_events(self, event):
    if event.key == pygame.K_RIGHT:
        self.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        self.ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()
    #elif event.key == pygame.K_SPACE:
      #  self._fire_bullet()


def _check_keyup_events(self, event):
    if event.key == pygame.K_RIGHT:
        self.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        self.ship.moving_left = False

# while loop that runs the game
while True:
    self._check_events()

    #use clock to slow down fps

    pygame.display.set_caption(f"Ships Ahoy {clock.get_fps():.0f}")
    screen.blit(bg, bg.get_rect())
    sunk_ship.draw()
    ship.update(wall_group)
    ship.draw(screen)
    pygame.sprite.Group.draw(wall_group, screen)

    #add score
    #img = font.render(f"Score: {score}", True, (255, 0, 0))

    pygame.display.flip()

    clock.tick(60)