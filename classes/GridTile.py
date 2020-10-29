import pygame

class GridTile:

    def __init__(self, game, type, pos):
        self.game = game

        self.set_type(type)

        self.pos = pos

        self.hover_square = pygame.Surface((50, 50))
        self.hover_square.set_alpha(32)
        self.hover_square.fill((255,255,255))

        self.selected_square = pygame.Surface((50, 50))
        self.selected_square.set_alpha(64)
        self.selected_square.fill((255,255,255))

        self.attack_wait_time = 0
        self.firing = False

        self.agro = False
        self.target = None

        self.level = 1

        self.upgrade_cost = 50

        self.font = pygame.font.Font("./assets/font.ttf", 16)


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
        self.game["display"].blit(self.sprite, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))
        #Draws transparent square on top if tile is hovered over
        if tuple(mouse_tile) == self.pos:
            self.game["display"].blit(self.hover_square, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))

