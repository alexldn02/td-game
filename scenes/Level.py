import pygame
from .Scene import Scene

class Level:
    def __init__(self, game_state, level_data):
        Scene.__init__(self, game_state)

        self.bg = pygame.image.load("./assets/levelbg.png")
        self.tile = pygame.image.load("./assets/tile.png")
    
    def show(self):
        self.game_state["display"].blit(self.bg, (0, 0))

        #Fills game grid with all 16x16 tiles
        for a in range(0,16):
            for b in range(0, 16):
                #50x50 pixels per grid tile, grid top left is at (435, 115)
                x = a*50 + 435
                y = b*50 + 115
                self.game_state["display"].blit(self.tile, (x, y))

        #Calls loop function that runs until scene is switched or game exited
        self.loop()

    def loop(self):
        #While loop to update the game rapidly that stops if the user quits the game
        crashed = False

        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            x, y = pygame.mouse.get_pos()

            #If mouse coords are within grid
            if x >= 435 and x < 1235 and y >= 115 and y < 915:
                #Calculates which tile of the grid the mouse is hovered over
                x_tile = (x - 435) // 50
                y_tile = (y - 115) // 50

                #Stores this mouse grid position in an array
                tile_on = [x_tile, y_tile]

                hover_square = pygame.Surface((50, 50))
                hover_square.set_alpha(128)
                hover_square.fill((255, 255, 255))
                self.game_state["display"].blit(hover_square, (x_tile*50 + 435, y_tile*50 + 115))


            pygame.display.update()
            self.game_state["clock"].tick(30)
