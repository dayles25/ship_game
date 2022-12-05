import pygame
import math

class Ship(pygame.sprite.Sprite):
    def __init__(self, sa_game):
        """Initialize the rocket and set its starting position."""
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.screen = sa_game.screen
        self.settings = sa_game.settings
        self.screen_rect = sa_game.screen.get_rect()

        self.image = pygame.image.load('images/Ships/ship (2).png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (33, 56))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()

        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right, self.moving_left = False, False
        self.moving_up, self.moving_down = False, False

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def center_ship(self):
        """Center the ship on the left side of the screen."""
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position.
        self.y = float(self.rect.y)
        self.x = 0

    def victory(self):
        if self.rect.right == self.screen_rect.right:
            return True

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
