import pygame
from pygame.sprite import Sprite

class SunkShip(Sprite):
    def __init__(self, screen):
        self.image = pygame.image.load('images/Ships/ship (19).png')
        self.rect = self.image.get_rect()
        self.x = 250
        self.y = 250
        self.screen = screen

    def draw(self):
        int_x = int(self.x)
        int_y = int(self.y)
        self.rect.center = (self.x, self.y)
        # twist the ship by theta
        # get a new rectangle for the updated/rotatd image
        rect = self.image.get_rect(center=self.rect.center)

        self.screen.blit(self.image, rect)