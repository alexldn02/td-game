import pygame
from .Button import Button

class CreateTowerButton(Button):

    def __init__(self, surface, type):

        self.surface = surface

        self.set_type(type)

        size = (self.bounds[0][1] - self.bounds[0][0], self.bounds[1][1] - self.bounds[1][0])

        self.hover_rect = pygame.Surface(size)
        self.hover_rect.set_alpha(32)
        self.hover_rect.fill((255,255,255))

        self.selected_rect = pygame.Surface(size)
        self.selected_rect.set_alpha(64)
        self.selected_rect.fill((255,255,255))

        self.disabled_rect = pygame.Surface(size)
        self.disabled_rect.set_alpha(64)
        self.disabled_rect.fill((0,0,0))


    def set_type(self, type):

        self.type = type

        if self.type == "basic":
            self.bounds = [[35, 345], [115, 225]]
            self.sprite = pygame.image.load("./assets/createbasicbtn.png")
            self.cost = 100

        elif self.type == "splash":
            self.bounds = [[35, 345], [245, 355]]
            self.sprite = pygame.image.load("./assets/createsplashbtn.png")
            self.cost = 120

        elif self.type == "sniper":
            self.bounds = [[35, 345], [375, 485]]
            self.sprite = pygame.image.load("./assets/createsniperbtn.png")
            self.cost = 140

        elif self.type == "flame":
            self.bounds = [[35, 345], [505, 615]]
            self.sprite = pygame.image.load("./assets/createflamebtn.png")
            self.cost = 160


    def update(self, mouse_pos, selected, money):
        #Blits sprite
        self.surface.blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        #Blits selected transparent rectangle if selected
        if selected == "create" + self.type:
            self.surface.blit(self.selected_rect, (self.bounds[0][0], self.bounds[1][0]))

        #Or disabled transparent rectangle if button is disabled
        elif money < self.cost:
            self.surface.blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))

        #Or hovered transparent rectangle if hovered over and not selected
        elif self.within_bounds(mouse_pos):
            self.surface.blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))