import pygame
from .Button import Button

class NextWaveButton(Button):

    def __init__(self, surface, type):
        self.bounds = [[35, 345], [775, 925]]

        super().__init__(surface, type)

        self.font = pygame.font.Font("./assets/font.ttf", 24)


    def set_type(self, type):
        self.type = type

        if self.type == "light":
            self.sprite = pygame.image.load("./assets/nextwavelightbtn.png")

        elif self.type == "medium":
            self.sprite = pygame.image.load("./assets/nextwavemediumbtn.png")

        elif self.type == "heavy":
            self.sprite = pygame.image.load("./assets/nextwaveheavybtn.png")

        elif self.type == "none":
            self.sprite = pygame.image.load("./assets/nextwavenonebtn.png")


    def update(self, mouse_pos, count = -1, time_left = -1):
        #Blits sprite
        self.surface.blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        #Blits text if next wave
        if self.type != "none":

            if not time_left == -1:
                time_left_text = self.font.render(str(time_left), True, (115,113,102))

                self.surface.blit(time_left_text, (94, 840))

            enemy_count_text = self.font.render(str(count), True, (0,0,0))

            if len(str(count)) == 1:
                self.surface.blit(enemy_count_text, (265, 875))
            else:
                self.surface.blit(enemy_count_text, (260, 875))      

        #Disabled transparent rectangle if button is disabled
        if self.type == "none":
            self.surface.blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))

        #Or hovered transparent rectangle if hovered over and not selected or disabled
        elif self.within_bounds(mouse_pos):
            self.surface.blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))