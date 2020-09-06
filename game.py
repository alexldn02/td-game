import pygame
from scenes.Scene import Scene
from scenes.TitleScene import TitleScene

#Starting up pygame module
pygame.init()

#Game state dictionary allows all current game information to be stored in one variable
#This means it can easily be passed on as a parameter for game objects
game_state = {}

game_state["width"] = 960
game_state["height"] = 720

#Using pygame to set parameters for the game window
game_state["display"] = pygame.display.set_mode((game_state["width"], game_state["height"])) #Window width and height
pygame.display.set_caption('TD Game') #Window title

#Setting up an in game clock
clock = pygame.time.Clock()

#Starts up the title scene
title_scene = TitleScene(game_state).show()

#While loop to update the game rapidly that stops if the user quits the game
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        
        #print(event)

    pygame.display.update()
    clock.tick(30)

#Shuts down pygame and current program when while loop ends
pygame.quit()
quit()