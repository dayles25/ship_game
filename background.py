import pygame

# 0 is water, 1 is sand
TILE_SIZE = 64

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

#def images
water = pygame.image.load("images/Tiles/rpgTile029.png")
# sand = pygame.image.load("images/PNG/Environment/dirt.png")

soils = [water]

#draw each tile to background
def draw_background(bg_size):
    bg = pygame.Surface(bg_size)
    # draw each tile onto our background
    for r, grid_list in enumerate(grid):
        for c, grid_element in enumerate(grid_list):
            # blit the correc tile onto our screen
            bg.blit(soils[grid_element], (c*TILE_SIZE, r*TILE_SIZE))
    return bg