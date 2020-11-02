import pygame
from leveldata import level_data
from .Scene import Scene
from .Level import Level
from .PlayLevelButton import PlayLevelButton
from .Button import Button

class LevelSelectScene(Scene):

    def __init__(self, game):

        self.game = game

        self.bg = pygame.image.load("./assets/levelselectbg.png")

        self.levels = []

        for level in level_data:
            self.levels.append(Level(self.game, level))


    def start(self):

        self.back_btn = Button(self.game, "back")

        self.play_level_btns = []

        for i in range (0, 5):
            self.play_level_btns.append(PlayLevelButton(self.game, (180 + 195*i, 90), i+1, True, 0))
        for i in range (0, 5):
            self.play_level_btns.append(PlayLevelButton(self.game, (960 -  195*i, 310), i+6, False, 0))
        for i in range (0, 5):
            self.play_level_btns.append(PlayLevelButton(self.game, (180 + 195*i, 530), i+11, False, 0))
        for i in range (0, 5):
            self.play_level_btns.append(PlayLevelButton(self.game, (960 -  195*i, 750), i+16, False, 0))

        self.mouse_pos = pygame.mouse.get_pos()

        self.game["display"].blit(self.bg, (0, 0))

        self.do_loop()


    def do_events(self):
            
            if self.event.type == pygame.MOUSEMOTION:

                self.mouse_pos = pygame.mouse.get_pos()

            if self.event.type == pygame.MOUSEBUTTONUP:
                
                if self.back_btn.within_bounds(self.mouse_pos):
                    self.stopped = True
                else:
                    for btn in self.play_level_btns:
                        if btn.within_bounds(self.mouse_pos) and btn.unlocked:
                            self.levels[btn.level].start()
                            self.start()


    def do_updates(self):

        self.back_btn.update(self.mouse_pos)

        for btn in self.play_level_btns:
            btn.update(self.mouse_pos)
