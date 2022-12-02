import pygame
import sys
from settings import Settings
from ship import Ship
from stats import Stats
import itertools
from random import random, randint, choice
from cannonball import Cannonball
from island import Island
from time import sleep
from button import Button
from scoreboard import Scoreboard
from ship2 import Ship2

class ShipsAhoy:
    '''class to manage game assets and behavior'''

    def __init__(self):
        '''Initialize game and create game resources'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Ships Ahoy")
        self.buffer = 150

        self.water = pygame.image.load("images/Tiles/rpgTile029.png")
        self.TILE_SIZE = 64

        self.ship = Ship(self)
        self.ship2 = Ship2(self)
        self.ships = pygame.sprite.Group()
        self.cannonballs = pygame.sprite.Group()
        self.islands = pygame.sprite.Group()

        self.play_button = Button(self, 'Play')
        self.stats = Stats(self)
        self.sb = Scoreboard(self)
        self.setup_map()

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self._check_cannonball_island_collisions()
                self._check_ship_cannonball_collisions()
                self._check_victory()
                self._create_cannonball()
                self.ship.update(self.islands)
                self.ship2.update(self.islands)
                self.cannonballs.update()
            self._update_screen()


    def _check_events(self):
        '''respond to keypress and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == ord('d'):
            self.ship2.moving_right = True
        elif event.key == ord('a'):
            self.ship2.moving_left = True
        if event.key == ord('w'):
            self.ship2.moving_up = True
        elif event.key == ord('s'):
            self.ship2.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        if event.key == ord('d'):
            self.ship2.moving_right = False
        elif event.key == ord('a'):
            self.ship2.moving_left = False
        if event.key == ord('w'):
            self.ship2.moving_up = False
        elif event.key == ord('s'):
            self.ship2.moving_down = False

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the play button is clicked'''
        # Hide Mouse
        pygame.mouse.set_visible(False)
        if self.play_button.rect.collidepoint(mouse_pos):
            #reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_ships2()

            # get rid of remaining groups
            self.islands.empty()
            self.setup_map()
            self.cannonballs.empty()

            #center ship and create another game
            self.ship.center_ship()
            self.ship2.center_ship()

    def get_random_position(self):
        '''Makes a random position tuple (x,y)'''
        x_loc = randint(0 + self.buffer, self.settings.screen_width - 2*self.buffer)
        y_loc = randint(0 + self.buffer, self.settings.screen_height - self.buffer)
        return (x_loc, y_loc)

    def setup_map(self):
        # build random islands
        for i in range(self.settings.obstacle_amount):
            new_island = Island(self.get_random_position(),
                                choice(['vertical', 'horizontal']))
            if not pygame.sprite.spritecollideany(new_island, self.islands):
                self.islands.add(new_island)
        if len(self.islands) < self.settings.obstacle_amount:
            for i in range(self.settings.obstacle_amount-len(self.islands)):
                new_island = Island(self.get_random_position(),
                                    choice(['vertical', 'horizontal']))
                if not pygame.sprite.spritecollideany(new_island, self.islands):
                    self.islands.add(new_island)


    def _check_cannonball_island_collisions(self):
        '''respond to bullet-alien collisions'''
        pygame.sprite.groupcollide(self.cannonballs, self.islands, True, False)

    def _check_ship_cannonball_collisions(self):
        '''check if cannonballs have hit the ship'''
        if pygame.sprite.spritecollide(self.ship, self.cannonballs, True):
            self._ship_hit()
        if pygame.sprite.spritecollide(self.ship2, self.cannonballs, True):
            self._ship2_hit()


    def _check_victory(self):
        '''check if ship has hit the right edge of the screen'''
        if self.ship.victory():
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.level += 1
            self.sb.prep_level()
            self.sb.check_high_score()
            self.ship2.center_ship()
        if self.ship2.victory():
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.stats.level += 1
            self.sb.prep_level()
            self.sb.check_high_score()
            self.ship2.center_ship()


    def _ship_hit(self):
        '''respond to ship being hit by alien'''
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.sb.prep_ships2()
            self.cannonballs.empty()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_level()
            self.sb.prep_ships()

    def _ship2_hit(self):
        '''respond to ship being hit by alien'''
        if self.stats.ships_left > 0:
            self.stats.ship2s_left -= 1
            self.sb.prep_ships2()
            self.sb.prep_ships()
            self.cannonballs.empty()
            self.ship2.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_level()
            self.sb.prep_ships2()

    def _create_cannonball(self):
        if random() < self.settings.cannonball_frequency:
            cannonball = Cannonball(self)
            self.cannonballs.add(cannonball)
            print(len(self.cannonballs))

    def _create_ship(self):
        self.ship.blitme()
        self.ship2.blitme()
        self.ships.add(self.ship)
        self.ships.add(self.ship2)


    def _update_cannonballs(self):
        """Update alien positions, and look for collisions with ship."""
        self.cannonballs.update()

        '''get rid of old cannonballs'''
        self.cannonballs.update()
        for cannonball in self.cannonballs:
            if cannonball.rect.bottom <= 0:
                self.cannonballs.remove(cannonball)

    def set_background(self):
        '''multiply water tiles across screen to fill background'''
        tile_height, tile_width = self.water.get_height(), self.water.get_width()
        for x, y in itertools.product(range(0, self.settings.screen_width, tile_width), range(0, self.settings.screen_height, tile_height)):
            self.screen.blit(self.water, (x, y))

    def _update_screen(self):
        '''update images on the screen, and flip to new screen'''
        self.set_background()
        self.islands.draw(self.screen)
        self.sb.show_score()
        self._create_ship()
        self.cannonballs.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    game = ShipsAhoy()
    game.run_game()