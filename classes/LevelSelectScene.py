import pygame
from leveldata import level_data
from .Scene import Scene
from .Level import Level
from .Button import Button

class LevelSelectScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.testlevel = Level(game, level_data[0])

        self.level1 = Level(self.game, level_data[1])
        self.level2 = Level(self.game, level_data[2])


    def start(self):

        self.back_btn = Button(self.game, "back")

        self.mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(self.game["display"], (120,120,120), (0, 0, 1280, 960))

        self.do_loop()


    def do_events(self):
            
            if self.event.type == pygame.MOUSEMOTION:

                self.mouse_pos = pygame.mouse.get_pos()

            if self.event.type == pygame.MOUSEBUTTONUP:
                
                if self.back_btn.within_bounds(self.mouse_pos):
                    self.stopped = True
                else:
                    self.testlevel.start()
                    self.start()
    
    def do_updates(self):

        self.back_btn.update(self.mouse_pos, None)