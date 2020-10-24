import pygame
from leveldata import level_data
from .Scene import Scene
from .Level import Level

class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.bg = pygame.image.load("./assets/titlebg.png")

        self.testlevel = Level(game, level_data[0])

        self.level1 = Level(game, level_data[1])
        self.level2 = Level(game, level_data[2])

    def start(self):
        
        self.do_loop()

    def do_events(self):
        if self.event.type == pygame.MOUSEBUTTONUP:
            self.testlevel.start()
            #self.level1.start()
            #self.level2.start()

    def do_updates(self):
        self.game["display"].blit(self.bg, (0, 0))