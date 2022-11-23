import pygame
import math
from wall import Wall

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Ships/ship (2).png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (33, 56))
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 300
        self.theta = 180
        self.speed = 0
        self.omega = 0


    def move_location(self, location):
        # move our rect to the passed in location
        self.rect.center = location

    def change_speed(self, delta=1):
        # stop angular movement
        # self.omega = 0
        # pass in +1 to move forward, -1 to move back
        if self.speed == 0:
            self.speed += delta
        elif self.speed == 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        self.speed = 0
        elif self.speed == -1:
            self.speed = 0

    def change_omega(self, delta=1):
        self.omega += delta

    def update(self, walls):
        theta_rads = math.pi / 180.0 * self.theta

        new_y = self.y + self.speed * math.cos(theta_rads)
        new_x = self.x + self.speed * math.sin(theta_rads)

        old_rect = self.rect
        self.rect.center = (new_x, new_y)

        if not pygame.sprite.spritecollide(self, pygame.sprite.Group(), False):
            self.x = new_x
            self.y = new_y
        else:
            print('collision')
            self.rect = old_rect

        # change angle based on arrow key
        self.theta -= self.omega

    def draw(self, screen):
        # now update the rectangle position
        int_x = int(self.x)
        int_y = int(self.y)
        self.rect.center = (self.x, self.y)
        # twist the ship by theta
        rot_ship = pygame.transform.rotate(self.image, self.theta)
        # get a new rectangle for the updated/rotatd image
        rot_rect = rot_ship.get_rect(center=self.rect.center)

        screen.blit(rot_ship, rot_rect)