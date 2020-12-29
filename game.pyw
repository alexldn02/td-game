import pygame
from classes.TitleScene import TitleScene

#Starting up pygame module
pygame.init()

#Game dictionary allows game display and clock to be stored in one variable
#This means it can easily be passed on as a parameter for game objects
game = {}

#Using pygame to set width, height and caption for game window
game["display"] = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("Confrontation")

#Setting up an in game clock
game["clock"] = pygame.time.Clock()

#Starts up the title scene
title_scene = TitleScene(game)
title_scene.start()

#Shuts down pygame and current program when while loop in Scene ends
pygame.quit()
quit()