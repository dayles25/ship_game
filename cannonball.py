import pygame

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, x, y, theta):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Ship parts/cannonBall.png')
        self.image = self.image.get_rect()
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = 3

    def update(self):
