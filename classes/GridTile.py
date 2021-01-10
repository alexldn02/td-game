import pygame

class GridTile:

    def __init__(self, surface, type, pos):
        self.surface = surface

        self.set_type(type)

        self.pos = pos

        #Transparent, white, square shaped Surface object that is blitted on top of the sprite to indicate it is hovered over
        self.hover_square = pygame.Surface((50, 50))
        self.hover_square.set_alpha(32)
        self.hover_square.fill((255,255,255))


    def set_type(self, type):
        self.type = type

        #Depending on what type the grid tile is, corresponding assets are loaded
        if self.type == "empty":
            self.sprite = pygame.image.load("./assets/tileempty.png")

        elif self.type == "wall":
            self.sprite = pygame.image.load("./assets/tilewall.png")

        elif self.type == "start":
            self.sprite = pygame.image.load("./assets/tilestart.png")

        elif self.type == "end":
            self.sprite = pygame.image.load("./assets/tileend.png")


    def update(self, mouse_tile):
        #Blits tile sprite
        self.surface.blit(self.sprite, (self.pos[0]*50, self.pos[1]*50))
        #Draws transparent square on top if tile is hovered over
        if tuple(mouse_tile) == self.pos:
            self.surface.blit(self.hover_square, (self.pos[0]*50, self.pos[1]*50))

