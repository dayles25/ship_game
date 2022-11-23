import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/Tiles/rpgTile029.png')
        self.rect = self.image.get_rect()
        self.rect.bottomright = pos

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)