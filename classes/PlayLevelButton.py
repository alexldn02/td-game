import pygame
from .Button import Button

class PlayLevelButton(Button):

    def __init__(self, surface, pos, level, unlocked, stars):
        
        self.surface = surface

        self.level = level

        self.unlocked = unlocked

        self.bounds = [[pos[0], pos[0] + 135], [pos[1], pos[1] + 160]]

        size = (self.bounds[0][1] - self.bounds[0][0], self.bounds[1][1] - self.bounds[1][0])

        self.hover_rect = pygame.Surface(size)
        self.hover_rect.set_alpha(32)
        self.hover_rect.fill((255,255,255))

        self.disabled_rect = pygame.Surface(size)
        self.disabled_rect.set_alpha(64)
        self.disabled_rect.fill((0,0,0))

        self.sprite = pygame.image.load("./assets/level" + str(stars) + "stars.png")

        self.font = pygame.font.Font("./assets/font.ttf", 64)


    def update(self, mouse_pos):
        #Blits sprite
        self.surface.blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))
        
        level_no = str(self.level)
        if len(level_no) == 1:
            level_no = "0" + str(self.level)

        text = self.font.render(level_no, True, (54,67,63))
        self.surface.blit(text, (self.bounds[0][0] + 30, self.bounds[1][0] + 30))
        
        #And disabled transparent rectangle if button is disabled
        if not self.unlocked:
            self.surface.blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))
            
        #Or hovered transparent rectangle if hovered over and not disabled
        elif self.within_bounds(mouse_pos):
            self.surface.blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))
