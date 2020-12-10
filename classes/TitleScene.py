import pygame
from .Scene import Scene
from .LevelSelectScene import LevelSelectScene
from .Button import Button

class TitleScene(Scene):

    def __init__(self, game):
        
        self.game = game

        self.bg = pygame.image.load("./assets/titlebg.png")

        self.level_select_scene = LevelSelectScene(self.game)


    def start(self):

        self.play_button = Button(self.game, "play")

        self.exit_button = Button(self.game, "exit")

        self.mouse_pos = pygame.mouse.get_pos()

        self.game["display"].blit(self.bg, (0, 0))
        
        self.do_loop()


    def do_events(self):

        if self.event.type == pygame.MOUSEMOTION:

            self.mouse_pos = pygame.mouse.get_pos()

        if self.event.type == pygame.MOUSEBUTTONUP:

            #If player clicks play button
            if self.play_button.within_bounds(self.mouse_pos):
                
                #Starts up the level selection scene
                self.level_select_scene.start()
                #When the level select scene do_loop is finished (player clicks back button in level select scene), title scene is restarted
                self.start()

            #If player clicks exit button
            elif self.exit_button.within_bounds(self.mouse_pos):

                #Closes the pygame window and ends the python script
                pygame.quit()
                quit()


    def do_updates(self):

        self.play_button.update(self.mouse_pos)

        self.exit_button.update(self.mouse_pos)
