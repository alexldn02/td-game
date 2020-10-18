import pygame
from classes.TitleScene import TitleScene
from classes.Level import Level

#Starting up pygame module
pygame.init()

#Game dictionary allows game display and clock to be stored in one variable
#This means it can easily be passed on as a parameter for game objects
game = {}

#This array contains data about how each level is defined
level_data = [{
        "startmoney": 50000,
        "tiles":[
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "waves":[{"type": "light", "count": 5}, {"type": "light", "count": 10}, {"type": "medium", "count": 5}]
        }]

#Width and height of game window
GAME_WIDTH = 1280
GAME_HEIGHT = 960

#Using pygame to set width, height and caption for game window
game["display"] = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Confrontation")

#Setting up an in game clock
game["clock"] = pygame.time.Clock()

#Starts up the title scene
#title_scene = TitleScene(game).start()

level1 = Level(game, level_data[0])
level1.start()

#Shuts down pygame and current program when while loop in Scene ends
pygame.quit()
quit()