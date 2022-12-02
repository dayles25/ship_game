import pygame
import sys
from settings import Settings
from ship import Ship
import itertools
from random import random, randint, choice
from cannonball import Cannonball
from island import Island
# from bullet import Bullet
from time import sleep
# from game_stats import GameStats
# from button import Button

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
        self.buffer = 40

        self.water = pygame.image.load("images/Tiles/rpgTile029.png")
        self.TILE_SIZE = 64


        # self.stats = GameStats(self)

        self.ship = Ship(self)
        self.cannonballs = pygame.sprite.Group()
        self.islands = pygame.sprite.Group()


        #self.bullets = pygame.sprite.Group()

        #self._create_fleet()
        #self.play_button = Button(self, 'Play')

        self.setup_map()

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()
            self._check_cannonball_island_collisions()
            #if self.stats.game_active:
            self._create_cannonball()
            self.ship.update()
            self.cannonballs.update()
            self._update_screen()


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
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        #elif event.key == pygame.K_SPACE:
        #    self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def get_random_position(self):
        '''Makes a random position tuple (x,y)'''
        x_loc = randint(0 + self.buffer, self.settings.screen_width - self.buffer)
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
            for i in range(self.settings.obstacle_amount):
                new_island = Island(self.get_random_position(),
                                    choice(['vertical', 'horizontal']))
                if not pygame.sprite.spritecollideany(new_island, self.islands):
                    self.islands.add(new_island)

    def _check_cannonball_island_collisions(self):
        '''respond to bullet-alien collisions'''
        pygame.sprite.groupcollide(self.cannonballs, self.islands, True, False)



    def _ship_hit(self):
        '''respond to ship being hit by alien'''
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.cannonballs.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False

#    def _update_aliens(self):
#        '''update positions of aliens in fleet'''
#        self._check_fleet_edges()
#        self.aliens.update()

#        if pygame.sprite.spritecollideany(self.ship, self.aliens):
#            self._ship_hit()

#        self._check_aliens_bottom()

#    def _create_alien(self, alien_number, row_number):
#        '''create an alien and place it in the row'''
#        alien = Alien(self)
#        alien_width, alien_height = alien.rect.size
#        alien.x = alien_width + 2 * alien_width * alien_number
#        alien.rect.x = alien.x
#        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
#        self.aliens.add(alien)

#    def _check_fleet_edges(self):
#        '''respond if any alien has hit the edge'''
#        for alien in self.aliens.sprites():
#            if alien.check_edges():
#                self._change_fleet_direction()
#                break

#    def _check_aliens_bottom(self):
#        '''check if aliens have reached the bottom of the screen'''
#        screen_rect = self.screen.get_rect()
#        for alien in self.aliens.sprites():
#            if alien.rect.bottom >= screen_rect.bottom:
#                self._ship_hit()
#                break

    def _create_cannonball(self):
        if random() < self.settings.cannonball_frequency:
            cannonball = Cannonball(self)
            self.cannonballs.add(cannonball)
            print(len(self.cannonballs))

    def _update_cannonballs(self):
        """Update alien positions, and look for collisions with ship."""
        self.cannonballs.update()

        '''get rid of old cannonballs'''
        self.cannonballs.update()
        for cannonball in self.cannonballs.copy():
            if cannonball.rect.bottom <= 0:
                self.cannonballs.remove(cannonball)

        #        self._check_bullet_alien_collisions()

    #  if pygame.sprite.spritecollideany(self.ship, self.aliens):
      #      self._ship_hit()

        # Look for aliens that have hit the left edge of the screen.
      #  self._check_cannonballs_left_edge()

    def _check_cannonballs_left_edge(self):
        """Respond to aliens that have hit left edge of the screen.
        Treat this the same as the ship getting hit.
        """

        for cannonball in self.cannonballs.sprites():
            if cannonball.rect.left < 0:
                self._ship_hit()
                break

    def set_background(self):
        tile_height, tile_width = self.water.get_height(), self.water.get_width()
        for x, y in itertools.product(range(0, self.settings.screen_width, tile_width), range(0, self.settings.screen_height, tile_height)):
            self.screen.blit(self.water, (x, y))

    def _update_screen(self):
        '''update images on the screen, and flip to new screen'''
        self.set_background()
        self.islands.draw(self.screen)
        self.ship.blitme()
        self.cannonballs.draw(self.screen)
        #for bullet in self.bullets.sprites():
            #bullet.draw_bullet()

       # self.aliens.draw(self.screen)
       # if not self.stats.game_active:
       #     self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    game = ShipsAhoy()
    game.run_game()