import pygame
import sys
from settings import Settings
from ship import Ship
import itertools
import random
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

        self.water = pygame.image.load("images/Tiles/rpgTile029.png")

        self.rock_1 = pygame.image.load('images/Tiles/tile_65.png')
        self.rock_2 = pygame.image.load('images/Tiles/tile_66.png')
        self.rock_3 = pygame.image.load('images/Tiles/tile_67.png')
    #    self.rocks = [rock_1, rock_2, rock_3]

        # self.stats = GameStats(self)

        self.ship = Ship(self)
        #self.bullets = pygame.sprite.Group()

        #self._create_fleet()
        #self.play_button = Button(self, 'Play')

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()
            #if self.stats.game_active:
            self.ship.update()
              #  self._update_bullets()
              #  self._update_aliens()
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

    #def _fire_bullet(self):
        '''creates new bullet and adds to group'''
     #   if len(self.bullets) < self.settings.bullets_allowed:
      #      new_bullet = Bullet(self)
       #     self.bullets.add(new_bullet)

#    def _update_bullets(self):
 #       '''Update position of bullets and get rid of old bullets'''
  #      self.bullets.update()
   #     for bullet in self.bullets.copy():
    #        if bullet.rect.bottom <= 0:
     #           self.bullets.remove(bullet)

#        self._check_bullet_alien_collisions()

#    def _check_bullet_alien_collisions(self):
#        '''respond to bullet-alien collisions'''
 #       collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
  #      if not self.aliens:
   #         self.bullets.empty()
    #        self._create_fleet()

#    def _ship_hit(self):
 #       '''respond to ship being hit by alien'''
  #      if self.stats.ships_left > 0:
   #         self.stats.ships_left -= 1
    #        self.aliens.empty()
     #       self.bullets.empty()
      #      self._create_fleet()
       #     self.ship.center_ship()
        #    sleep(0.5)
#        else:
 #           self.stats.game_active = False

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

    def set_background(self):
        tile_height, tile_width = self.water.get_height(), self.water.get_width()
        for x, y in itertools.product(range(0, self.settings.screen_width, tile_width), range(0, self.settings.screen_height, tile_height)):
            self.screen.blit(self.water, (x, y))

    def create_obstacles(self, amount):
     #   random_x = random.randint(200, 1000)
     #   random_y = random.randint(50, 590)
     #   random_rock = random.choice(self.rocks)
     #   for x in range(amount):
        self.screen.blit(self.rock_1, (200, 300))
        self.screen.blit(self.rock_2, (400, 100))
        self.screen.blit(self.rock_3, (700, 150))
        self.screen.blit(self.rock_1, (1000, 300))
        self.screen.blit(self.rock_2, (600, 500))


    def _update_screen(self):
        '''update images on the screen, and flip to new screen'''
        self.set_background()
        self.create_obstacles(self.settings.obstacle_amount)
        self.ship.blitme()
        #for bullet in self.bullets.sprites():
            #bullet.draw_bullet()

       # self.aliens.draw(self.screen)
       # if not self.stats.game_active:
       #     self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    game = ShipsAhoy()
    game.run_game()