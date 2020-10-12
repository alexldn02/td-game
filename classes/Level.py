import pygame
from .Scene import Scene
from .GridTile import GridTile
from .Enemy import Enemy
from .Button import Button

#Level class that inherits Scene where most of the games code will be
class Level(Scene):

    def __init__(self, game, level_data):
        super().__init__(game)

        self.level_data = level_data

        #Loading up assets needed in scene
        self.bg = pygame.image.load("./assets/levelbg.png")

        self.font = pygame.font.Font("./assets/font.ttf", 24)


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
                elif self.level_data["tiles"][b][a] == 2:
                    tile_type = "start"
                    self.start_tile = (a, b)
                #Or end type if they are defined as the end tile
                elif self.level_data["tiles"][b][a] == 3:
                    tile_type = "end"
                    self.end_tile = (a, b)
                #Otherwise they are given the empty type
                else:
                    tile_type = "empty"

                tile = GridTile(self.game, tile_type, [a, b])

                self.grid[a].append(tile)

        #Active enemies are also represented in an array, each enemy being an object
        self.enemies = []

        #Waves are taken from level_data
        self.waves = self.level_data["waves"]

        self.wave_no = -1

        #Money value is set to whatever it is defined as for the particular level
        self.money = self.level_data["startmoney"]

        #Health is set to max
        self.health = 100

        #Buttons are instantiated
        self.back_btn = Button(self.game, "back")
        self.create_basic_btn = Button(self.game, "createbasic")
        self.create_splash_btn = Button(self.game, "createsplash")
        self.create_sniper_btn = Button(self.game, "createsniper")
        self.create_incendiary_btn = Button(self.game, "createincendiary")
        self.next_wave_btn = Button(self.game, "nextwave" + self.waves[0]["type"])

        #Stores which option on the left of the grid has been selected, defaults to "none"
        self.selected = "none"

        #Stores the position of the mouse in an array
        self.mouse_pos = pygame.mouse.get_pos()

        #Stores the x and y of the tile that the mouse is over, or -1 if mouse is not over the grid
        self.mouse_tile = [-1, -1]
        
        #Level background image is blitted to the scene
        self.game["display"].blit(self.bg, (0, 0))

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

                #If tile clicked is not taken up by wall or tower
                if self.grid[x][y].get_type() == "empty":
                    #Depending on which button is selected, specified tower is created
                    if self.selected == "createbasic":
                        self.grid[x][y].set_type("towerbasic")
                        self.selected = "none"
                        self.money -= 100

                    elif self.selected == "createsplash":
                        self.grid[x][y].set_type("towersplash")
                        self.selected = "none"
                        self.money -= 100

                    elif self.selected == "createsniper":
                        self.grid[x][y].set_type("towersniper")
                        self.selected = "none"
                        self.money -= 100

                    elif self.selected == "createincendiary":
                        self.grid[x][y].set_type("towerincendiary")
                        self.selected = "none"
                        self.money -= 100

            else:
                #If mouse clicks within within bounds of a button and has enough money it is selected
                if self.create_basic_btn.within_bounds(self.mouse_pos) and self.money >= 100:
                    if self.selected == "createbasic":
                        self.selected = "none"
                    else:
                        self.selected = "createbasic"

                elif self.create_splash_btn.within_bounds(self.mouse_pos) and self.money >= 100:
                    if self.selected == "createsplash":
                        self.selected = "none"
                    else:
                        self.selected = "createsplash"

                elif self.create_sniper_btn.within_bounds(self.mouse_pos) and self.money >= 100:
                    if self.selected == "createsniper":
                        self.selected = "none"
                    else:
                        self.selected = "createsniper"

                elif self.create_incendiary_btn.within_bounds(self.mouse_pos) and self.money >= 100:
                    if self.selected == "createincendiary":
                        self.selected = "none"
                    else:
                        self.selected = "createincendiary"

                elif self.next_wave_btn.within_bounds(self.mouse_pos) and self.wave_no < len(self.waves) - 1:
                    self.start_next_wave()
                    

    def do_updates(self):
        #After events are handled, all sprites are updated

        #Health bar is updated
        pygame.draw.rect(self.game["display"], (255, 255, 255), (60, 25, 225, 15))
        pygame.draw.rect(self.game["display"], (197, 9, 9), (60, 25, self.health * 2.25, 15))

        #Money display is updated
        pygame.draw.rect(self.game["display"], (219, 178, 111), (60, 65, 85, 25))
        self.money_text = self.font.render(str(self.money), True, (0,0,0))
        self.game["display"].blit(self.money_text, (64, 67))
        
        #Back button is updated
        self.back_btn.update(self.mouse_pos)

        #Tower create buttons are updated
        self.create_basic_btn.update(self.mouse_pos, self.selected)
        self.create_splash_btn.update(self.mouse_pos, self.selected)
        self.create_sniper_btn.update(self.mouse_pos, self.selected)
        self.create_incendiary_btn.update(self.mouse_pos, self.selected)

        #Next wave button is updated
        self.next_wave_btn.update(self.mouse_pos)

        #Every tile in the grid is updated
        for tile_y in self.grid:
            for tile_x in tile_y:
                tile_x.update(self.mouse_tile)

        #Enemies are updated
        for enemy in self.enemies:
            if enemy.is_alive():
                if enemy.is_moved():
                    enemy.move(self.grid)

                enemy.update()


    def start_next_wave(self):
        self.wave_no += 1
        self.current_wave = self.waves[self.wave_no]

        if self.wave_no == len(self.waves) - 1:
            self.next_wave_btn.set_type("wavesend")
        else:
            self.next_wave = self.waves[self.wave_no + 1]
            self.next_wave_btn.set_type("nextwave" + self.next_wave["type"])

        for i in range(0, self.current_wave["count"]):
            self.enemies.append(Enemy(self.game, self.current_wave["type"], self.start_tile, self.end_tile))


    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.grid)
