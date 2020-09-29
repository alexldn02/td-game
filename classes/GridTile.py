import pygame

class GridTile:

    def __init__(self, game_state, type, pos):
        self.game_state = game_state

        self.type = type

        self.pos = pos

        if self.type == "empty":
            self.sprite = pygame.image.load("./assets/tile.png")
            self.sprite_hovered = pygame.image.load("./assets/tilehovered.png")
        elif self.type == "wall":
            self.sprite = pygame.image.load("./assets/wall.png")
            self.sprite_hovered = pygame.image.load("./assets/wallhovered.png")
        elif self.type == "start":
            self.sprite = pygame.image.load("./assets/start.png")
            self.sprite_hovered = pygame.image.load("./assets/starthovered.png")
        elif self.type == "end":
            self.sprite = pygame.image.load("./assets/end.png")
            self.sprite_hovered = pygame.image.load("./assets/endhovered.png")
        elif self.type == "towerbasic":
            self.sprite = pygame.image.load("./assets/towerbasic.png")
            self.sprite_hovered = pygame.image.load("./assets/towerbasichovered.png")
        elif self.type == "towersplash":
            self.sprite = pygame.image.load("./assets/towersplash.png")
            self.sprite_hovered = pygame.image.load("./assets/towersplashhovered.png")
        elif self.type == "towersniper":
            self.sprite = pygame.image.load("./assets/towersniper.png")
            self.sprite_hovered = pygame.image.load("./assets/towersniperhovered.png")
        elif self.type == "towerincendiary":
            self.sprite = pygame.image.load("./assets/towerincendiary.png")
            self.sprite_hovered = pygame.image.load("./assets/towerincendiaryhovered.png")

    def get_type(self):
        return self.type

    def get_pos(self):
        return self.pos

    def update(self, mouse_tile):
        if mouse_tile == self.pos:
                self.game_state["display"].blit(self.sprite_hovered, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))
        else:
            self.game_state["display"].blit(self.sprite, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))

