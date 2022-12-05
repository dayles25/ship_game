import pygame
import pygame.font
import sys
from settings import Settings
from ship import Ship
from stats import Stats
import itertools
from random import random, randint, choice
from cannonball import Cannonball
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

        #set up screen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Ships Ahoy")

        #define water tile and size
        self.water = pygame.image.load("images/Tiles/rpgTile029.png")
        self.TILE_SIZE = 64

        #define font for game
        self.font = pygame.font.SysFont('Gigi', 48)

        #initialize ships and add sprites to groups
        self.ship = Ship(self)
        self.ship2 = Ship2(self)
        self.ships = pygame.sprite.Group()
        self.cannonballs = pygame.sprite.Group()

        # create and intialize game attributes
        self.play_button = Button(self, 'Play')
        self.stats = Stats(self)
        self.sb = Scoreboard(self)

        # load sounds
        self.hit_sound = pygame.mixer.Sound("sounds/eep.wav")
        self.dead_sound = pygame.mixer.Sound("sounds/scream.wav")
        pygame.mixer.music.load("sounds/background_music.wav")

    def run_game(self):
        '''Start the main loop for the game'''
        #play music
        pygame.mixer.music.play(-1)
        #main loop for the game
        while True:
            self._check_events()
            if self.stats.game_active:
                self._check_ship_cannonball_collisions()
                self._check_victory()
                self._create_cannonball()
                self.ship.update()
                self.ship2.update()
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
        #check for keydown events
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # WASD controls
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
        #check for keyup events
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        #WASD controls
        if event.key == ord('d'):
            self.ship2.moving_right = False
        elif event.key == ord('a'):
            self.ship2.moving_left = False
        if event.key == ord('w'):
            self.ship2.moving_up = False
        elif event.key == ord('s'):
            self.ship2.moving_down = False

    def end_game(self):
        '''Ends the game, displays score, and resets score'''
        while True:
            self.screen.fill((138, 19, 19))
            #score message
            img = self.font.render(f"Score: {self.stats.level}", True, (20, 20, 20))
            img_rect = img.get_rect()
            img_rect.midbottom = self.screen.get_rect().midbottom
            self.screen.blit(img, img_rect)
            #game over message
            img_1 = self.font.render(f"GAME OVER - Press Spacebar to restart", True, (20, 20, 20))
            img_1_rect = img_1.get_rect()
            img_1_rect.center = self.screen.get_rect().center
            self.screen.blit(img_1, img_1_rect)
            #quit message
            img_2 = self.font.render(f"QUIT GAME - Press Q", True, (20, 20, 20))
            img_2_rect = img_2.get_rect()
            img_2_rect.midtop = self.screen.get_rect().midtop
            self.screen.blit(img_2, img_2_rect)

            pygame.display.flip()
            # get events to reset the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    # respond to spacebar
                    if event.key == pygame.K_SPACE:

                        self.stats.reset_stats()
                        self.stats.game_active = True
                        self.stats.level = 1
                        self.sb.prep_level()
                        self.sb.prep_ships()
                        self.sb.prep_ships2()

                        # get rid of remaining groups
                        self.cannonballs.empty()

                        # center ship and create another game
                        self.ship.center_ship()
                        self.ship2.center_ship()
                    #disregard other keys besides q
                    else:
                        continue
                    #kill game over screen
                    return 0

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the play button is clicked'''
        # Hide Mouse
        pygame.mouse.set_visible(False)
        if self.play_button.rect.collidepoint(mouse_pos):
            #reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            # reset level
            self.stats.level = 1
            # prep scoring mechanisms
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_ships2()

            # get rid of remaining groups
            self.cannonballs.empty()

            #center ship and create another game
            self.ship.center_ship()
            self.ship2.center_ship()


    def _check_ship_cannonball_collisions(self):
        '''check if cannonballs have hit the ship'''
        # if collision is sensed, execute the repective ship_hit function
        if pygame.sprite.spritecollide(self.ship, self.cannonballs, True):
            self._ship_hit()
        if pygame.sprite.spritecollide(self.ship2, self.cannonballs, True):
            self._ship2_hit()



    def _check_victory(self):
        '''check if ship has hit the right edge of the screen'''
        # see if ship has hit the edge and update the game accordingly
        if self.ship.victory():
            #recenter ships
            self.ship.center_ship()
            self.ship2.center_ship()
            #update level
            self.stats.level += 1
            #increase difficulty
            self.settings.increase_speed()
            # prep scoring functions
            self.sb.prep_level()
            self.sb.check_high_score()

        if self.ship2.victory():
            self.ship.center_ship()
            self.ship2.center_ship()
            self.stats.level += 1
            self.settings.increase_speed()
            self.sb.prep_level()
            self.sb.check_high_score()



    def _ship_hit(self):
        '''respond to ship being hit by cannonball'''
        if self.stats.ships_left > 0:
            pygame.mixer.Sound.play(self.hit_sound)
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.sb.prep_ships2()
            self.ship.center_ship()
            sleep(0.5)
        else:
            #kill ship and end game
            pygame.mixer.Sound.play(self.dead_sound)
            self.stats.game_active = False
            self.sb.prep_level()
            self.sb.prep_ships()
            self.end_game()

    def _ship2_hit(self):
        '''respond to ship being hit by cannonball'''
        if self.stats.ship2s_left > 0:
            pygame.mixer.Sound.play(self.hit_sound)
            #update health bar
            self.stats.ship2s_left -= 1
            #prep scoring features
            self.sb.prep_ships2()
            self.sb.prep_ships()
            self.ship2.center_ship()
            sleep(0.5)
        else:
            #kill ship and end game
            pygame.mixer.Sound.play(self.dead_sound)
            self.stats.game_active = False
            # prep scoring features
            self.sb.prep_level()
            self.sb.prep_ships2()
            #end game
            self.end_game()

    def _create_cannonball(self):
        #spawn random cannonballs on the right side of the screen
        if random() < self.settings.cannonball_frequency:
            cannonball = Cannonball(self)
            self.cannonballs.add(cannonball)
            print(len(self.cannonballs))

    def _create_ship(self):
        #create and add ship to ships group
        self.ship.blitme()
        self.ship2.blitme()
        self.ships.add(self.ship)
        self.ships.add(self.ship2)


    def _update_cannonballs(self):
        """Update cannonball positions, and look for collisions with ship."""
        self.cannonballs.update()

        '''get rid of old cannonballs once they leave the screen'''
        self.cannonballs.update()
        for cannonball in self.cannonballs:
            if cannonball.rect.bottom <= 0:
                self.cannonballs.remove(cannonball)

    def set_background(self):
        '''multiply water tiles across screen to fill background'''
        #use water tiles to create ocean background
        #itertools allows creator to iterate an image over a set range
        tile_height, tile_width = self.water.get_height(), self.water.get_width()
        for x, y in itertools.product(range(0, self.settings.screen_width, tile_width), range(0, self.settings.screen_height, tile_height)):
            self.screen.blit(self.water, (x, y))

    def _update_screen(self):
        '''update images on the screen, and flip to new screen'''
        # input elements that must be constantly updated
        self.set_background()
        self.sb.show_score()
        self._create_ship()
        self.cannonballs.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        #display the updated screen
        pygame.display.flip()

#run game
if __name__ == '__main__':
    game = ShipsAhoy()
    game.run_game()