import pygame
import random
import math
import collections

class Enemy:

    def __init__(self, game, type, start_tile, end_tile):
        self.game = game        

        self.alive = True

        self.moved = True

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
            
        elif self.type == "medium":
            self.sprite = pygame.image.load('./assets/enemymedium.png')
            self.middle = [7, 9]
            self.speed = 0.3
            self.health = 40
            
        elif self.type == "heavy":
            self.sprite = pygame.image.load('./assets/enemyheavy.png')
            self.middle = [7, 10]
            self.speed = 0.1
            self.health = 80

        self.current_pos = [self.current_tile[0]*50 + random.randint(0, 50) + 435, self.current_tile[1]*50 + random.randint(0, 50) + 115]
        self.dest_pos = ()

        self.sprite_rot = pygame.transform.rotate(self.sprite, 0)

    def move(self, grid):

        self.moved = False

        self.dest_tile = self.find_path(grid, self.current_tile)[1]

        self.dest_pos = (self.dest_tile[0]*50 + random.randint(5, 45) + 435, self.dest_tile[1]*50 + random.randint(5, 45) + 115)

        self.move_distance = ((self.dest_pos[0] - self.current_pos[0])**2 + (self.dest_pos[1] - self.current_pos[1])**2)**0.5

        self.move_vector = [self.speed * ((self.dest_pos[0] - self.current_pos[0]) / self.move_distance), self.speed * ((self.dest_pos[1] - self.current_pos[1]) / self.move_distance)]

        radians = math.atan2(self.dest_pos[1] - self.current_pos[1], self.dest_pos[0] - self.current_pos[0])
        self.move_angle = 270 - math.degrees(radians)
        
        self.sprite_rot = pygame.transform.rotate(self.sprite, self.move_angle)

    def find_path(self, grid, start):

        #Shortest path algorithm (breadth first)
        queue = collections.deque([[start]])
        
        seen = set([start])
        
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if grid[x][y].get_type() == "end":
                return path
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if 0 <= x2 < 16 and 0 <= y2 < 16 and (grid[x2][y2].get_type() == "empty" or grid[x2][y2].get_type() == "end" or grid[x2][y2].get_type() == "start") and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def update(self):

        if round(self.current_pos[0]) != round(self.dest_pos[0]):
            self.current_pos[0] += self.move_vector[0]

        if round(self.current_pos[1]) != round(self.dest_pos[1]):
            self.current_pos[1] += self.move_vector[1]

        elif round(self.current_pos[1]) == round(self.dest_pos[1]) and round(self.current_pos[0]) == round(self.dest_pos[0]):
            self.current_tile = self.dest_tile
            if self.current_tile == self.end_tile:
                print("damage")
                self.alive = False
            else:
                self.moved = True
        
        blit_pos = (self.current_pos[0] - self.middle[0], self.current_pos[1] - self.middle[1])
        self.game["display"].blit(self.sprite_rot, blit_pos)

    def is_moved(self):
        return self.moved

    def is_alive(self):
        return self.alive

    def get_tile(self):
        return self.current_tile
