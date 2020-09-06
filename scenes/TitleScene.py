import pygame
from .Scene import Scene

class TitleScene(Scene):
    def __init__(self, game_state):
        Scene.__init__(self, game_state)

        print('New Title Scene Class')

        self.bg = pygame.image.load('./assets/titlebackground.png')

    def show(self):
        self.game_state["display"].blit(self.bg, (0, 0))