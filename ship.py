import pygame
from pygame.sprite import Sprite
import math

class Ship(Sprite):
    def __init__(self, screen):
        self.image = pygame.image.load('images/Ships/ship (2).png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (33, 56))
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 200
        self.theta = 0
        self.speed = 0
        self.omega = 0
        self.screen = screen

    def move_location(self, location):
        # move our rect to the passed in location
        self.rect.center = location

    def change_speed(self, delta=1):
        # stop angular movement
        self.omega = 0
        # pass in +1 to move forward, -1 to move back
        self.speed += delta

    def change_omega(self, delta=1):
        # stop linear movement
        self.speed = 0
        self.omega += delta

    def update(self):
        # update the position based on speed
        # convert theta to radians
        theta_rads = math.pi / 180.0 * self.theta
        self.y += self.speed * math.cos(theta_rads)
        self.x += self.speed * math.sin(theta_rads)
        # change angle based on arrow key OLD FEATURE
        self.theta -= self.omega

        # NEW FEATURE CHANGE ANGLE BASED ON MOUSE
        # get the mouse cursor
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # delta_x = mouse_x - self.x
        #cdelta_y = self.y - mouse_y
        # find the angle to mouse and pass to ship theta
        # self.theta = math.atan2(delta_y, delta_x) * 180 / math.pi + 90
        # check if mouse pressed and fire bullet
        # if pygame.mouse.get_pressed()[0]:
            # fire a bullet here
            # pass

    def draw(self):
        # now update the rectangle position
        int_x = int(self.x)
        int_y = int(self.y)
        self.rect.center = (self.x, self.y)
        # twist the ship by theta
        rot_ship = pygame.transform.rotate(self.image, self.theta)
        # get a new rectangle for the updated/rotatd image
        rot_rect = rot_ship.get_rect(center=self.rect.center)

        self.screen.blit(rot_ship, rot_rect)