import pygame
import datetime

#Generic Scene class, all game scenes will be children of this class
class Scene:

    def __init__(self, game_state):

        self.game_state = game_state


    def do_loop(self):
        #While loop to update the game rapidly that stops if the user quits the game
        stopped = False

        while not stopped:
            #Iterates through every event recieved from pygame
            for self.event in pygame.event.get():

                #Causes loop to stop if game is exited
                if self.event.type == pygame.QUIT:
                    stopped = True

                #Performs event checks found in child classes
                self.do_events()

            #Updates the game at 60fps
            pygame.display.update()
            self.game_state["clock"].tick(60)
            print(datetime.datetime.now().time())
            #print(self.game_state["clock"])

    def do_events(self):
        return
