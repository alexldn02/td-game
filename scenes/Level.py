import pygame
from .Scene import Scene

class Level(Scene):
    def __init__(self, game_state, level_data):
        Scene.__init__(self, game_state)

        #Loading up assets needed in scene
        self.bg = pygame.image.load("./assets/levelbg.png")

        self.tile = pygame.image.load("./assets/tile.png")
        self.tile_hovered = pygame.image.load("./assets/tilehovered.png")
        self.wall = pygame.image.load("./assets/wall.png")
        self.wall_hovered = pygame.image.load("./assets/wallhovered.png")
        self.start = pygame.image.load("./assets/start.png")
        self.start_hovered = pygame.image.load("./assets/starthovered.png")
        self.end = pygame.image.load("./assets/end.png")
        self.end_hovered = pygame.image.load("./assets/endhovered.png")

        self.tower_basic = pygame.image.load("./assets/towerbasic.png")
        self.tower_basic_hovered = pygame.image.load("./assets/towerbasichovered.png")
        self.tower_splash = pygame.image.load("./assets/towersplash.png")
        self.tower_splash_hovered = pygame.image.load("./assets/towersplashhovered.png")
        self.tower_sniper = pygame.image.load("./assets/towersniper.png")
        self.tower_sniper_hovered = pygame.image.load("./assets/towersniperhovered.png")
        self.tower_incendiary = pygame.image.load("./assets/towerincendiary.png")
        self.tower_incendiary_hovered = pygame.image.load("./assets/towerincendiaryhovered.png")

        #Grid is represented as a 2D array, tiles are represented as dictionaries within array
        self.grid = []
        for a in range(0, 16):
            self.grid.append([])
            for b in range(0,16):
                self.grid[a].append([])

                #Tiles are given the wall type if they are defined as walls in level_data
                if level_data["tiles"][b][a] == 1:
                    tiletype = "wall"
                #Or start type if they are defined as the start tile
                elif level_data["tiles"][b][a] == "start":
                    tiletype = "start"
                #Or end type if they are defined as the end tile
                elif level_data["tiles"][b][a] == "end":
                    tiletype = "end"
                #Otherwise they are given the empty type
                else:
                    tiletype = "empty"

                self.grid[a][b] = {
                        "type": tiletype,
                        "level": -1
                    }

        #Money value is set to whatever it is defined as for the particular level
        self.money = level_data["startmoney"]

    
    def show(self):
        #Level background image is blitted to the scene first thing
        self.game_state["display"].blit(self.bg, (0, 0))

        #Stores which option on the left of the grid has been selected, defaults to "none"
        self.selected = "none"

        #While loop to update the game rapidly that stops if the user quits the game
        exit_window = False

        while not exit_window:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    #Causes loop to stop
                    exit_window = True

                if event.type == pygame.MOUSEMOTION:
                    #Every time the mouse is moved its position is tracked
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
                    
                    #If mouse is in grid
                    if x_tile != -1 and y_tile != -1:
                        #On tile that mouse is over the hovered version of the sprite is blitted
                        if self.grid[x_tile][y_tile]["type"] == "wall":
                            self.game_state["display"].blit(self.wall_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                        elif self.grid[x_tile][y_tile]["type"] == "start":
                            self.game_state["display"].blit(self.start_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                        elif self.grid[x_tile][y_tile]["type"] == "end":
                            self.game_state["display"].blit(self.end_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                        elif self.grid[x_tile][y_tile]["type"] == "towerbasic":
                            self.game_state["display"].blit(self.tower_basic_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                        elif self.grid[x_tile][y_tile]["type"] == "towersplash":
                            self.game_state["display"].blit(self.tower_splash_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                        elif self.grid[x_tile][y_tile]["type"] == "towersniper":
                            self.game_state["display"].blit(self.tower_sniper_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                        elif self.grid[x_tile][y_tile]["type"] == "towerincendiary":
                            self.game_state["display"].blit(self.tower_incendiary_hovered, (x_tile*50 + 435, y_tile*50 + 115))

                        else:
                            self.game_state["display"].blit(self.tile_hovered, (x_tile*50 + 435, y_tile*50 + 115))

                    #Iterates through every tile in the grid
                    for a in range(0, 16):
                        for b in range(0, 16):
                            if not (a == x_tile and b == y_tile):
                                #On all tiles that are not hovered over regular sprites are blitted
                                if self.grid[a][b]["type"] == "wall":
                                    self.game_state["display"].blit(self.wall, (a*50 + 435, b*50 + 115))
                                elif self.grid[a][b]["type"] == "start":
                                    self.game_state["display"].blit(self.start, (a*50 + 435, b*50 + 115))
                                elif self.grid[a][b]["type"] == "end":
                                    self.game_state["display"].blit(self.end, (a*50 + 435, b*50 + 115))

                                elif self.grid[a][b]["type"] == "towerbasic":
                                    self.game_state["display"].blit(self.tower_basic, (a*50 + 435, b*50 + 115))
                                elif self.grid[a][b]["type"] == "towersplash":
                                    self.game_state["display"].blit(self.tower_splash, (a*50 + 435, b*50 + 115))
                                elif self.grid[a][b]["type"] == "towersniper":
                                    self.game_state["display"].blit(self.tower_sniper, (a*50 + 435, b*50 + 115))
                                elif self.grid[a][b]["type"] == "towerincendiary":
                                    self.game_state["display"].blit(self.tower_incendiary, (a*50 + 435, b*50 + 115))
                                    
                                else:
                                    self.game_state["display"].blit(self.tile, (a*50 + 435, b*50 + 115))

                if event.type == pygame.MOUSEBUTTONUP:
                    #If mouse clicks and is within grid
                    if x_tile != -1 and y_tile != -1:
                        #If tile mouse is over is not taken up by wall or tower
                        if self.grid[x_tile][y_tile]["type"] == "empty":
                            #Depending on which button is selected, specified tower is created
                            if self.selected == "createbasic":
                                #Tile becomes basic tower
                                self.grid[x_tile][y_tile]["type"] = "towerbasic"
                                self.game_state["display"].blit(self.tower_basic_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                            elif self.selected == "createsplash":
                                #Tile becomes splash tower
                                self.grid[x_tile][y_tile]["type"] = "towersplash"
                                self.game_state["display"].blit(self.tower_splash_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                            elif self.selected == "createsniper":
                                #Tile becomes sniper tower
                                self.grid[x_tile][y_tile]["type"] = "towersniper"
                                self.game_state["display"].blit(self.tower_sniper_hovered, (x_tile*50 + 435, y_tile*50 + 115))
                            elif self.selected == "createincendiary":
                                #Tile becomes incendiary tower
                                self.grid[x_tile][y_tile]["type"] = "towerincendiary"
                                self.game_state["display"].blit(self.tower_incendiary_hovered, (x_tile*50 + 435, y_tile*50 + 115))

            pygame.display.update()
            self.game_state["clock"].tick(60)


    def getLevelData(self):
        return self.level_data
