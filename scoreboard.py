import pygame.font
from pygame.sprite import Group

from ship import Ship
from ship2 import Ship2


class Scoreboard:
    '''reports scoring info'''

    def __init__(self, sa_game):
        '''Initialize scorekeeping attributes'''
        self.sa_game = sa_game
        self.screen = sa_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sa_game.settings
        self.stats = sa_game.stats

        #font settings
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_level()
        self.prep_high_score()
        self.prep_ships()
        self.prep_ships2()

    def prep_level(self):
        '''turn the score into an image'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        #display score top right
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 20

    def prep_high_score(self):
        '''turn high score into rendered image'''
        high_score = self.stats.high_score
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        #center high score on top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.level_rect.top

    def show_score(self):
        '''draw scores to the screen'''
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)
        self.ships2.draw(self.screen)

    def check_high_score(self):
        '''check to see if new high score'''
        if self.stats.level > self.stats.high_score:
            self.stats.high_score = self.stats.level
            self.prep_high_score()

    def prep_ships(self):
        '''show how many ships are left'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.sa_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_ships2(self):
        '''lives of ghost ship'''
        self.ships2 = Group()
        for ship_number in range(self.stats.ship2s_left):
            ship2 = Ship2(self.sa_game)
            ship2.rect.x = 10 + ship_number * ship2.rect.width
            ship2.rect.y = 50
            self.ships.add(ship2)
