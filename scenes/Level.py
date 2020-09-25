import pygame
from .Scene import Scene

class Level:
    def __init__(self, game_state, level_data):
        Scene.__init__(self, game_state)

        self.level_data = level_data

        #Loading up assets needed in scene
        self.bg = pygame.image.load("./assets/levelbg.png")
        self.tile = pygame.image.load("./assets/tile.png")
        self.tile_hovered = pygame.image.load("./assets/tilehovered.png")

        #Grid is represented as a 2D array, tiles are represented as dictionaries within array
        self.grid = []
        for a in range(0, 16):
            self.grid.append([])
            for b in range(0,16):
                self.grid[a].append([])

                self.grid[a][b] = {
                    "hovered": False,
                    "wall": False,
                    "tower": False
                }

    
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

            mouse = pygame.mouse.get_pos()

            #If mouse coords are within grid
            if mouse[0] >= 435 and mouse[0] < 1235 and mouse[1] >= 115 and mouse[1] < 915:
                #Calculates which tile of the grid the mouse is hovered over
                x_tile = (mouse[0] - 435) // 50
                y_tile = (mouse[1] - 115) // 50
            else:
                x_tile = -1
                y_tile = -1
            print(x_tile, y_tile)

            self.grid[x_tile][y_tile]["hovered"] = True
            if not (x_tile == -1 or y_tile == -1):
                self.game_state["display"].blit(self.tile_hovered, (x_tile*50 + 435, y_tile*50 + 115))
            for a in range(0, 16):
                for b in range(0, 16):
                    if not (a == x_tile and b == y_tile):
                        self.grid[a][b]["hovered"] = False
                        self.game_state["display"].blit(self.tile, (a*50 + 435, b*50 + 115))



            pygame.display.update()
            self.game_state["clock"].tick(60)

    def getLevelData(self):
        return self.level_data
