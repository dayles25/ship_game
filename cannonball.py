import pygame
from random import randint

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, sa_game):
        super().__init__()
        self.screen = sa_game.screen
        self.settings = sa_game.settings

        self.image = pygame.image.load('images/Ship parts/cannonBall.png')
        self.rect = self.image.get_rect()


        self.rect.left = self.screen.get_rect().right
        cannonball_top_max = self.settings.screen_height - self.rect.height
        self.rect.top = randint(0, cannonball_top_max)

        self.x = float(self.rect.x)

    def update(self):
        self.x -= self.settings.alien_speed
        self.rect.x = self.x