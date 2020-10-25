import pygame
import collections
import math
from .Scene import Scene
from .GridTile import GridTile
from .Tower import Tower
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
        self.start_tiles = []

        for a in range(0, 16):
            self.grid.append([])

            for b in range(0,16):
                #Tiles are given the wall type if they are defined as walls in level_data
                if self.level_data["tiles"][b][a] == 1:
                    tile_type = "wall"
                #Or start type if they are defined as the start tile
                elif self.level_data["tiles"][b][a] == 2:
                    tile_type = "start"
                    self.start_tiles.append((a, b))
                #Or end type if they are defined as the end tile
                elif self.level_data["tiles"][b][a] == 3:
                    tile_type = "end"
                    self.end_tile = (a, b)
                #Otherwise they are given the empty type
                else:
                    tile_type = "empty"

                tile = GridTile(self.game, tile_type, (a, b))

                self.grid[a].append(tile)

        #Active enemies are also represented in an array, each enemy being an object
        self.enemies = []

        #Waves are taken from level_data
        self.waves = self.level_data["waves"]

        self.wave_no = -1

        #Money value is set to whatever initial value it is defined as for the particular level
        self.money = self.level_data["startmoney"]

        #Health is set to max
        self.health = 100

        #Buttons are instantiated
        self.back_btn = Button(self.game, "back")
        self.create_basic_btn = Button(self.game, "createbasic")
        self.create_splash_btn = Button(self.game, "createsplash")
        self.create_sniper_btn = Button(self.game, "createsniper")
        self.create_flame_btn = Button(self.game, "createflame")
        self.upgrade_tower_btn = Button(self.game, "upgradetower")
        self.delete_tower_btn = Button(self.game, "deletetower")
        self.next_wave_btn = Button(self.game, "nextwave" + self.waves[0]["type"])

        #Stores what is currently selected by the player
        #Either holds a string representing a button, a tuple representing a tile in the grid, or None
        self.selected = None

        #Stores the position of the mouse in an array
        self.mouse_pos = pygame.mouse.get_pos()

        #Stores the x and y of the tile that the mouse is over, or -1 if mouse is not over the grid
        self.mouse_tile = [-1, -1]

        #Timers are set to 0
        self.next_wave_timer = 0
        self.level_end_timer = 0

        #Stores waves that are in the process of spawning
        self.current_waves = []

        #Changes to True when player wins the level
        self.won = False

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
                if self.grid[x][y].type == "empty":
                    enemy_here = False
                    for enemy in self.enemies:
                        if enemy.alive:
                            if enemy.current_tile == tuple(self.mouse_tile) or enemy.dest_tile == tuple(self.mouse_tile):
                                enemy_here = True

                    #A tower can be built if it does not block the path and the tile is not currently being used by an enemy
                    path = True
                    for start_tile in self.start_tiles:
                        if not self.is_path(start_tile, (x, y)):
                            path = False
                    if path and not enemy_here:
                        #Depending on which button is selected, specified tower is created
                        if self.selected == "createbasic":
                            self.grid[x][y] = Tower(self.game, "basic", (x, y))
                            self.selected = None
                            self.money -= 100

                        elif self.selected == "createsplash":
                            self.grid[x][y] = Tower(self.game, "splash", (x, y))
                            self.selected = None
                            self.money -= 120

                        elif self.selected == "createsniper":
                            self.grid[x][y] = Tower(self.game, "sniper", (x, y))
                            self.selected = None
                            self.money -= 140

                        elif self.selected == "createflame":
                            self.grid[x][y] = Tower(self.game, "flame", (x, y))
                            self.selected = None
                            self.money -= 160

                        else:
                            self.selected = None

                elif isinstance(self.grid[x][y], Tower):
                    if self.selected == (x, y):
                        self.selected = None
                    else:
                        self.selected = (x, y)

                else:
                    self.selected = None
                

            #If mouse clicks, not within grid
            else:
                #Button selection
                #If mouse clicks within within bounds of a button and has enough money it is selected
                if self.create_basic_btn.within_bounds(self.mouse_pos) and self.money >= 100:
                    if self.selected == "createbasic":
                        self.selected = None
                    else:
                        self.selected = "createbasic"

                elif self.create_splash_btn.within_bounds(self.mouse_pos) and self.money >= 120:
                    if self.selected == "createsplash":
                        self.selected = None
                    else:
                        self.selected = "createsplash"

                elif self.create_sniper_btn.within_bounds(self.mouse_pos) and self.money >= 140:
                    if self.selected == "createsniper":
                        self.selected = None
                    else:
                        self.selected = "createsniper"

                elif self.create_flame_btn.within_bounds(self.mouse_pos) and self.money >= 160:
                    if self.selected == "createflame":
                        self.selected = None
                    else:
                        self.selected = "createflame"

                elif self.upgrade_tower_btn.within_bounds(self.mouse_pos) and type(self.selected) == tuple and self.money >= 50:
                    if self.grid[self.selected[0]][self.selected[1]].level < 10:
                        self.grid[self.selected[0]][self.selected[1]].level_up()
                        self.money -= 50

                elif self.delete_tower_btn.within_bounds(self.mouse_pos) and type(self.selected) == tuple:
                    self.grid[self.selected[0]][self.selected[1]] = GridTile(self.game, "empty", self.selected)
                    self.selected = None

                #If player clicks "next wave" and there are waves remaining
                elif self.next_wave_btn.within_bounds(self.mouse_pos) and self.wave_no < len(self.waves) - 1:
                    self.start_next_wave()

                elif self.back_btn.within_bounds(self.mouse_pos):
                    self.stopped = True

                else:
                    self.selected = None
                    
        if self.event.type == pygame.KEYUP:
            if self.event.key == pygame.K_ESCAPE:
                self.selected = None

    def do_updates(self):
        #After events are handled, all objects are updated
        #Sprites/shapes at the back of the scene have to be updated first and sprites/shapes at the front last

        #Health bar is updated
        if self.health < 0:
            self.health = 0
        pygame.draw.rect(self.game["display"], (64, 53, 41), (60, 25, 225, 15))
        pygame.draw.rect(self.game["display"], (197, 9, 9), (60, 25, self.health * 2.25, 15))

        #Money display is updated
        pygame.draw.rect(self.game["display"], (219, 178, 111), (60, 65, 85, 25))
        money_text = self.font.render(str(self.money), True, (0,0,0))
        self.game["display"].blit(money_text, (64, 67))
        
        #Back button is updated
        self.back_btn.update(self.mouse_pos, self.selected)

        #Tower create buttons are updated
        self.create_basic_btn.update(self.mouse_pos, self.selected)
        self.create_splash_btn.update(self.mouse_pos, self.selected)
        self.create_sniper_btn.update(self.mouse_pos, self.selected)
        self.create_flame_btn.update(self.mouse_pos, self.selected)

        #Tower action buttons are updated
        self.upgrade_tower_btn.update(self.mouse_pos, self.selected)
        self.delete_tower_btn.update(self.mouse_pos, self.selected)

        #Next wave button is updated
        if self.wave_no == len(self.waves) - 1:
            wave_count = -1
        else:
            wave_count = self.waves[self.wave_no + 1]["count"]

        if self.wave_no == len(self.waves) - 1:
            time_left = -1
        elif self.waves[self.wave_no + 1]["time"] == -1:
            time_left = -1
        else:
            time_left = math.ceil((self.waves[self.wave_no + 1]["time"]*60 - self.next_wave_timer) / 60)
        
        self.next_wave_btn.update(self.mouse_pos, self.selected, wave_count, time_left)

        #Every tile in the grid is updated
        for row in self.grid:
            for tile in row:
                #If the tile is a tower, enemies array is also given as an argument
                if isinstance(tile, Tower):
                    tile.update(self.mouse_tile, self.selected, self.enemies)
                else:
                    tile.update(self.mouse_tile)

        #Tower attack animations are updated
        for row in self.grid:
            for tile in row:
                #If the tile is a tower
                if isinstance(tile, Tower):
                    if tile.agro:
                        tile.update_attack_anim()

        #All enemies are updated
        for enemy in self.enemies:
            if enemy.damaging:
                self.health -= enemy.damage
                enemy.damaging = False
            #Only live enemies are rendered
            if enemy.alive:
                #If enemy has finished a movement, it immediately performs the next
                if enemy.moved:
                    enemy.move(self.grid)
                enemy.update()
            elif enemy.to_reward:
                self.money += enemy.reward
                enemy.to_reward = False

        #Health bars of enemies are updated after enemies so that they are blitted in front
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update_health_bar()

        #For every wave that is currently spawning
        for current_wave in self.current_waves:
            #First enemy is spawned immediately
            if current_wave["spawned"] == 0:
                self.enemies.append(Enemy(self.game, current_wave["info"]["type"], self.start_tiles[current_wave["info"]["starttile"]], self.end_tile))
                current_wave["spawned"] += 1

            current_wave["timer"] += 1

            #Next enemies are spawned one every second (60 frames)
            if current_wave["timer"] == 60 and current_wave["info"]["count"] > 1:
                self.enemies.append(Enemy(self.game, current_wave["info"]["type"], self.start_tiles[current_wave["info"]["starttile"]], self.end_tile))
                current_wave["spawned"] += 1

                if current_wave["spawned"] == current_wave["info"]["count"]:
                    self.current_waves.remove(current_wave)
                    current_wave["spawned"] = 0

                current_wave["timer"] = 0

        #Next wave automatically starts when time is up
        self.next_wave_timer += 1

        if self.wave_no != len(self.waves) - 1:
            if self.next_wave_timer == self.waves[self.wave_no + 1]["time"] * 60:
                self.start_next_wave()

        #Checks if level has been won
        enemies_alive = False
        for enemy in self.enemies:
            if enemy.alive:
                enemies_alive = True
        
        if self.wave_no == len(self.waves) - 1 and not enemies_alive:
            #Waits 2 seconds, then level ends
            if self.level_end_timer == 120 and not self.won:
                self.won = True
            else:
                self.level_end_timer += 1


    def start_next_wave(self):
        #Starts the next wave of enemies
        self.wave_no += 1

        if not "starttile" in self.waves[self.wave_no]:
            self.waves[self.wave_no]["starttile"] = 0

        #New wave is added to currently spawning waves
        self.current_waves.append({
            "info": self.waves[self.wave_no],
            "spawned": 0,
            "timer": 0
        })

        #If the wave begun is the last wave, next wave button is set to no new waves type
        if self.wave_no == len(self.waves) - 1:
            self.next_wave_btn.set_type("wavesend")
        #Otherwise it is set to display whatever wave is next
        else:
            self.next_wave_btn.set_type("nextwave" + self.waves[self.wave_no + 1]["type"])

        #Next wave timer is reset
        self.next_wave_timer = 0

    
    def is_path(self, start, new_tower):
        #When a new tower is to be placed, this method determines whether it blocks the enemies path or not
        #Towers can only be placed if they do not block the path entirely
        #A breadth-first shortest path algorithm is used to calculate this
        
        grid = self.grid
        new_tower = tuple(new_tower)

        #The algorithm uses a queue data type to build the path
        queue = collections.deque([[start]])

        #Stores all the tiles that have been "seen" by the algorithm
        seen = set([start])
        
        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if grid[x][y].type == "end":
                #If no path could be made, returns false
                if path == None:
                    return False
                #If a path could be made, returns True
                else:
                    return True

            #For every tile that neighbours the current x, y
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                #Evaluates to True if tile is not a wall or tower
                does_not_block = grid[x2][y2].type == "empty" or grid[x2][y2].type == "end" or grid[x2][y2].type == "start"
                #If coord is within the range of the grid, is not currently taken up by wall or tower,
                #will not be taken up by the new tower once placed, and has not been seen yet
                if 0 <= x2 < 16 and 0 <= y2 < 16 and does_not_block and (x2, y2) != new_tower and (x2, y2) not in seen:
                    #The coord along with the current path is appended to the queue
                    queue.append(path + [(x2, y2)])
                    #The coord is added to seen
                    seen.add((x2, y2))
