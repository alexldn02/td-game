import pygame
import random
import math
import collections

class Enemy:

    def __init__(self, game, type, start_tile, end_tile):
        self.game = game        

        self.alive = True

        self.moved = True

        self.damaging = False

        self.type = type
        self.current_tile = start_tile
        self.dest_tile = ()
        self.end_tile = end_tile

        #Appropriate sprites are loaded and the middle of the sprite in pixels is defined
        #so that they can be blitted using their centre coordinate insstead of top left
        if self.type == "light":
            self.sprite = pygame.image.load('./assets/enemylight.png')
            self.middle = [5, 8]
            self.speed = 0.5
            self.health = 20
            self.damage = 5
            
        elif self.type == "medium":
            self.sprite = pygame.image.load('./assets/enemymedium.png')
            self.middle = [7, 9]
            self.speed = 0.3
            self.health = 40
            self.damage = 10
            
        elif self.type == "heavy":
            self.sprite = pygame.image.load('./assets/enemyheavy.png')
            self.middle = [7, 10]
            self.speed = 0.1
            self.health = 80
            self.damage = 20

        self.current_pos = [self.current_tile[0]*50 + random.randint(0, 50) + 435, self.current_tile[1]*50 + random.randint(0, 50) + 115]
        self.dest_pos = ()

        self.sprite_rot = pygame.transform.rotate(self.sprite, 0)


    def move(self, grid):

        self.moved = False

        #The enemy finds the next tile it is to move to according to shortest path algorithm        
        self.dest_tile = self.find_path(grid, self.current_tile)[1]

        #A random point within the destination tile is chosen for the enemy to move to
        self.dest_pos = (self.dest_tile[0]*50 + random.randint(5, 45) + 435, self.dest_tile[1]*50 + random.randint(5, 45) + 115)

        self.move_distance = ((self.dest_pos[0] - self.current_pos[0])**2 + (self.dest_pos[1] - self.current_pos[1])**2)**0.5

        self.move_vector = [self.speed * ((self.dest_pos[0] - self.current_pos[0]) / self.move_distance), self.speed * ((self.dest_pos[1] - self.current_pos[1]) / self.move_distance)]

        radians = math.atan2(self.dest_pos[1] - self.current_pos[1], self.dest_pos[0] - self.current_pos[0])
        self.move_angle = 360 - math.degrees(radians)
        
        self.sprite_rot = pygame.transform.rotate(self.sprite, self.move_angle)


    def find_path(self, grid, start):
        #When enemies move, they must find a path to get to the end tile
        #A breadth-first shortest path algorithm is used to calculate this
        queue = collections.deque([[start]])
        
        seen = set([start])
        
        while queue:
            path = queue.popleft()
            x, y = path[-1]

            #Once the end tile is checked, the path is complete and is returned
            if grid[x][y].type == "end":
                return path

            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                #Evaluates to True if tile is not a wall or tower
                does_not_block = grid[x2][y2].type == "empty" or grid[x2][y2].type == "end" or grid[x2][y2].type == "start"
                #If coord is within the range of the grid, is not taken up by wall or tower,
                #and has not been seen yet
                if 0 <= x2 < 16 and 0 <= y2 < 16 and does_not_block and (x2, y2) not in seen:
                    #The coord along with the current path is appended to the queue
                    queue.append(path + [(x2, y2)])
                    #The coord is added to seen
                    seen.add((x2, y2))


    def update(self):

        if round(self.current_pos[0]) != round(self.dest_pos[0]):
            self.current_pos[0] += self.move_vector[0]

        if round(self.current_pos[1]) != round(self.dest_pos[1]):
            self.current_pos[1] += self.move_vector[1]

        elif round(self.current_pos[1]) == round(self.dest_pos[1]) and round(self.current_pos[0]) == round(self.dest_pos[0]):
            self.current_tile = self.dest_tile
            if self.current_tile == self.end_tile:
                self.damaging = True
                self.alive = False
            else:
                self.moved = True
        
        if self.health <= 0:
            self.alive = False
        
        blit_pos = (self.current_pos[0] - self.middle[0], self.current_pos[1] - self.middle[1])
        self.game["display"].blit(self.sprite_rot, blit_pos)
