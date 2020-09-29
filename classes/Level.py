import pygame
from .Scene import Scene
from .GridTile import GridTile
from .Enemy import Enemy
from .Button import Button

#Level class that inherits Scene where most of the games code will be
class Level(Scene):

    def __init__(self, game_state, level_data):
        Scene.__init__(self, game_state)

        self.level_data = level_data

        #Loading up assets needed in scene
        self.bg = pygame.image.load("./assets/levelbg.png")

        self.back_btn = pygame.image.load("./assets/backbtn.png")
        self.back_btn_hovered = pygame.image.load("./assets/backbtnhovered.png")


    def start(self):
        #Grid is represented as a 2D array, tiles are represented as objects within array
        self.grid = []

        for a in range(0, 16):
            self.grid.append([])

            for b in range(0,16):
                #Tiles are given the wall type if they are defined as walls in level_data
                if self.level_data["tiles"][b][a] == 1:
                    tile_type = "wall"
                #Or start type if they are defined as the start tile
                elif self.level_data["tiles"][b][a] == "start":
                    tile_type = "start"
                #Or end type if they are defined as the end tile
                elif self.level_data["tiles"][b][a] == "end":
                    tile_type = "end"
                #Otherwise they are given the empty type
                else:
                    tile_type = "empty"

                tile = GridTile(self.game_state, tile_type, [a, b])

                self.grid[a].append(tile)

        #Money value is set to whatever it is defined as for the particular level
        self.money = self.level_data["startmoney"]

        #Level background image is blitted to the scene first thing
        self.game_state["display"].blit(self.bg, (0, 0))

        self.create_basic_btn = Button(self.game_state, "createbasic")
        self.create_splash_btn = Button(self.game_state, "createsplash")
        self.create_sniper_btn = Button(self.game_state, "createsniper")
        self.create_incendiary_btn = Button(self.game_state, "createincendiary")

        self.game_state["display"].blit(self.back_btn, (1105, 10))

        #Stores which option on the left of the grid has been selected, defaults to "none"
        self.selected = "none"

        #Stores the position of the mouse in an array
        self.mouse_pos = pygame.mouse.get_pos()

        #Stores the x and y of the tile that the mouse is over, or -1 if mouse is not over the grid
        self.mouse_tile = [-1, -1]

        #Starts loop from method found in parent Scene class
        self.do_loop()


    def do_events(self):

        if self.event.type == pygame.MOUSEMOTION:

            #Every time the mouse is moved its position is tracked
            self.mouse_pos = pygame.mouse.get_pos()
            
            #If mouse coords are within grid
            if self.mouse_pos[0] >= 435 and self.mouse_pos[0] < 1235 and self.mouse_pos[1] >= 115 and self.mouse_pos[1] < 915:
                #Calculates which tile of the grid the mouse is hovered over
                tile_x = (self.mouse_pos[0] - 435) // 50
                tile_y = (self.mouse_pos[1] - 115) // 50
                self.mouse_tile = [tile_x, tile_y]
            else:
                #Position is stored as -1 if mouse is not over the grid
                self.mouse_tile = [-1, -1]

            
 
        if self.event.type == pygame.MOUSEBUTTONUP:

            #If mouse clicks and is within grid
            if self.mouse_tile != [-1, -1]:

                x = self.mouse_tile[0]
                y = self.mouse_tile[1]

                #If tile mouse is over is not taken up by wall or tower
                if self.grid[x][y].get_type() == "empty":
                    #Depending on which button is selected, specified tower is created
                    if self.selected == "createbasic":
                        #Tile becomes basic tower
                        self.grid[x][y].set_type("towerbasic")
                        self.selected = "none"
                    elif self.selected == "createsplash":
                        #Tile becomes splash tower
                        self.grid[x][y].set_type("towersplash")
                        self.selected = "none"
                    elif self.selected == "createsniper":
                        #Tile becomes sniper tower
                        self.grid[x][y].set_type("towersniper")
                        self.selected = "none"
                    elif self.selected == "createincendiary":
                        #Tile becomes incendiary tower
                        self.grid[x][y].set_type("towerincendiary")
                        self.selected = "none"

            else:
                if self.create_basic_btn.within_bounds(self.mouse_pos):
                    if self.selected == "createbasic":
                        self.selected = "none"
                    else:
                        self.selected = "createbasic"
                elif self.create_splash_btn.within_bounds(self.mouse_pos):
                    if self.selected == "createsplash":
                        self.selected = "none"
                    else:
                        self.selected = "createsplash"
                elif self.create_sniper_btn.within_bounds(self.mouse_pos):
                    if self.selected == "createsniper":
                        self.selected = "none"
                    else:
                        self.selected = "createsniper"
                elif self.create_incendiary_btn.within_bounds(self.mouse_pos):
                    if self.selected == "createincendiary":
                        self.selected = "none"
                    else:
                        self.selected = "createincendiary"

        self.create_basic_btn.update(self.mouse_pos, self.selected)
        self.create_splash_btn.update(self.mouse_pos, self.selected)
        self.create_sniper_btn.update(self.mouse_pos, self.selected)
        self.create_incendiary_btn.update(self.mouse_pos, self.selected)

        for tile_x in self.grid:
            for tile_y in tile_x:
                tile_y.update(self.mouse_tile)


    def find_path(self):
        return
