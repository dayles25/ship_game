import pygame

class Island(pygame.sprite.Sprite):
    def __init__(self, pos, orientation='horizontal'):
        # init sprite:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Tiles/tile_66.png')
        # assume wall is horizontal unless set to vertical
        if orientation == 'vertical':
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)