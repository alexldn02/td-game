import pygame
from .Scene import Scene
from .LevelSelectScene import LevelSelectScene
from .Button import Button

class TitleScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.bg = pygame.image.load("./assets/titlebg.png")

        self.level_select_scene = LevelSelectScene(self.game)


    def start(self):

        self.play_button = Button(self.game, "play")

        self.mouse_pos = pygame.mouse.get_pos()

        self.game["display"].blit(self.bg, (0, 0))
        
        self.do_loop()


    def do_events(self):

        if self.event.type == pygame.MOUSEMOTION:

            self.mouse_pos = pygame.mouse.get_pos()

        if self.event.type == pygame.MOUSEBUTTONUP:

            if self.play_button.within_bounds(self.mouse_pos):
                
                self.level_select_scene.start()
                self.start()


    def do_updates(self):

        self.play_button.update(self.mouse_pos, None)
