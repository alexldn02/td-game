import pygame
from .Button import Button

class CreateTowerButton(Button):

    def __init__(self, game, type):

        self.game = game

        self.set_type(type)

        size = (self.bounds[0][1] - self.bounds[0][0], self.bounds[1][1] - self.bounds[1][0])

        self.hover_rect = pygame.Surface(size)
        self.hover_rect.set_alpha(32)
        self.hover_rect.fill((255,255,255))

        self.selected_rect = pygame.Surface(size)
        self.selected_rect.set_alpha(64)
        self.selected_rect.fill((255,255,255))


    def set_type(self, type):

        self.type = type

        if self.type == "basic":
            self.bounds = [[35, 345], [115, 225]]
            self.sprite = pygame.image.load("./assets/createbasicbtn.png")

        elif self.type == "splash":
            self.bounds = [[35, 345], [245, 355]]
            self.sprite = pygame.image.load("./assets/createsplashbtn.png")

        elif self.type == "sniper":
            self.bounds = [[35, 345], [375, 485]]
            self.sprite = pygame.image.load("./assets/createsniperbtn.png")

        elif self.type == "flame":
            self.bounds = [[35, 345], [505, 615]]
            self.sprite = pygame.image.load("./assets/createflamebtn.png")


    def update(self, mouse_pos, selected):
        #Blits sprite
        self.game["display"].blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        #Blits selected transparent rectangle if selected
        if selected == "create" + self.type:
            self.game["display"].blit(self.selected_rect, (self.bounds[0][0], self.bounds[1][0]))

        #Or hovered transparent rectangle if hovered over and not selected
        elif self.within_bounds(mouse_pos):
            self.game["display"].blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))