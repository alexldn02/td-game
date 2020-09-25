import pygame
from .Scene import Scene

class Level(Scene):
    def __init__(self, game_state, level_data):
        Scene.__init__(self, game_state)

        self.level_data = level_data

        #Loading up assets needed in scene
        self.bg = pygame.image.load("./assets/levelbg.png")
        self.tile = pygame.image.load("./assets/tile.png")
        self.tile_wall = pygame.image.load("./assets/tilewall.png")
        self.tile_hovered = pygame.image.load("./assets/tilehovered.png")
        self.tile_wall_hovered = pygame.image.load("./assets/tilewallhovered.png")

        #Grid is represented as a 2D array, tiles are represented as dictionaries within array
        self.grid = []
        for a in range(0, 16):
            self.grid.append([])
            for b in range(0,16):
                self.grid[a].append([])

                #Tiles are given the wall type if they are defined as walls in level_data
                if self.level_data["walls"][b][a] == 1:
                    self.grid[a][b] = {
                        "hovered": False,
                        "type": "wall",
                    }
                #Otherwise they are given the empty type
                else:
                    self.grid[a][b] = {
                        "hovered": False,
                        "type": "empty",
                    }

    
    def show(self):
        self.game_state["display"].blit(self.bg, (0, 0))

        mouse = pygame.mouse.get_pos()

        #While loop to update the game rapidly that stops if the user quits the game
        crashed = False

        while not crashed:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    crashed = True

                if event.type == pygame.MOUSEMOTION:

                    mouse = pygame.mouse.get_pos()
                    
                    #If mouse coords are within grid
                    if mouse[0] >= 435 and mouse[0] < 1235 and mouse[1] >= 115 and mouse[1] < 915:
                        #Calculates which tile of the grid the mouse is hovered over
                        x_tile = (mouse[0] - 435) // 50
                        y_tile = (mouse[1] - 115) // 50
                    else:
                        #Position is stored as -1 if mouse is not over the grid
                        x_tile = -1
                        y_tile = -1
                    print(x_tile, y_tile)

                    self.grid[x_tile][y_tile]["hovered"] = True
                    if not (x_tile == -1 or y_tile == -1):
                        if self.grid[x_tile][y_tile]["type"] == "wall":
                                self.game_state["display"].blit(self.tile_wall_hovered, (x_tile*50 + 435, y_tile*50 + 115))                    
                        else:
                            self.game_state["display"].blit(self.tile_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                    for a in range(0, 16):
                        for b in range(0, 16):
                            if not (a == x_tile and b == y_tile):
                                self.grid[a][b]["hovered"] = False
                                if self.grid[a][b]["type"] == "wall":
                                    self.game_state["display"].blit(self.tile_wall, (a*50 + 435, b*50 + 115))
                                else:
                                    self.game_state["display"].blit(self.tile, (a*50 + 435, b*50 + 115))



            pygame.display.update()
            self.game_state["clock"].tick(60)


    def getLevelData(self):
        return self.level_data
