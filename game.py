import pygame
from scenes.Scene import Scene
from scenes.TitleScene import TitleScene
from scenes.Level import Level

#Starting up pygame module
pygame.init()

#Game state dictionary allows all current game information to be stored in one variable
#This means it can easily be passed on as a parameter for game objects
game_state = {}

game_state["width"] = 1280
game_state["height"] = 960

#Using pygame to set parameters for the game window
game_state["display"] = pygame.display.set_mode((game_state["width"], game_state["height"])) #Window width and height
pygame.display.set_caption("Confrontation") #Window title

#Setting up an in game clock
game_state["clock"] = pygame.time.Clock()

#Starts up the title scene
#title_scene = TitleScene(game_state).show()

level1 = Level(game_state, 0).show()

#Shuts down pygame and current program when while loop ends
pygame.quit()
quit()