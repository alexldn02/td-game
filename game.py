from scenes.Scene import Scene
from scenes.TitleScene import TitleScene

#Starting up pygame module
import pygame

pygame.init()

#Using pygame to set parameters for the game window
GAME_WIDTH = 960
GAME_HEIGHT = 720

gameDisplay = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) #Window width and height
pygame.display.set_caption('Battle Lines') #Window title

#Setting up an in game clock
clock = pygame.time.Clock()

title_scene = TitleScene()

#While loop to update the game state that stops if the user quits the game
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