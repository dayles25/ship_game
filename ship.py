import pygame
import math

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Ships/ship (2).png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (33, 56))
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 200
        self.theta = 0
        self.speed = 0
        self.omega = 0

    def move_location(self, location):
        # move our rect to the passed in location
        self.rect.center = location

    def change_speed(self, delta=1):
        # stop angular movement
        # self.omega = 0
        # pass in +1 to move forward, -1 to move back
        self.speed += delta

    def change_omega(self, delta=1):
        self.omega += delta

    def update(self, walls):
        # update the position based on speed
        # convert theta to radians
        theta_rads = math.pi / 180.0 * self.theta

        self.y = self.y + self.speed * math.cos(theta_rads)
        self.x = self.x + self.speed * math.sin(theta_rads)

        # if not pygame.sprite.spritecollide()
        # self.x = new_x
        # self.y = new_y

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