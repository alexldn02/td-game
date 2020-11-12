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

        save_file = open("./save.data", "r")
        
        save_data = save_file.readlines()

        #First line of save file represents the level the player is up to
        current_level = int(save_data[0])

        self.back_btn = Button(self.game, "back")

        self.play_level_btns = []
        level_no = 0
        for row in range(0, 4):
            for column in range(0, 5):
                level_no += 1

                if row % 2 == 0:
                    x = 180 + 195*column
                else:
                    x = 960 -  195*column
                
                y = 90 + 220*row

                #Level is unlocked if level player is up to is greater or equal to this level
                unlocked = current_level >= level_no

                #Each line of save file after the first represents the number of stars the player has completed that level with
                stars = int(save_data[level_no])

                self.play_level_btns.append(PlayLevelButton(self.game, (x, y), level_no, unlocked, stars))

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
