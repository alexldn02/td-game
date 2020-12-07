import pygame
import sys

#Generic Scene class, all game scenes will be children of this class
class Scene:

    def do_loop(self):
        
        self.stopped = False

        #While loop to update the scene rapidly
        while not self.stopped:

            try:

                #Iterates through every event recieved from pygame
                for self.event in pygame.event.get():

                    #If player clicks "x" button program quits
                    if self.event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    #Performs event checks found in child classes
                    self.do_events()

                #Performs updates found in child classes
                self.do_updates()

                #Updates the game at 60fps
                #If PC game is ran on cannot run at 60fps, in game "seconds" will be slower
                pygame.display.update()
                self.game["clock"].tick(60)
                #print(self.game["clock"].get_fps())

            except:
                print(sys.exc_info()[0])
                pygame.quit()
                quit()
            

    def do_events(self):
        return

    def do_updates(self):
        return
