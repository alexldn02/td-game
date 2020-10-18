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

        self.fire_damage = 0
        self.on_fire_timer = 0

        self.type = type

        self.current_tile = start_tile
        self.dest_tile = ()
        self.end_tile = end_tile

        #Appropriate sprites are loaded and the middle of the sprite in pixels is defined
        #so that they can be blitted using their centre coordinate insstead of top left
        if self.type == "light":
            self.sprite = pygame.image.load('./assets/enemylight.png')
            self.middle = (5, 8)
            self.speed = 0.5
            self.max_health = 20
            self.damage = 5
            self.reward = 10
            
        elif self.type == "medium":
            self.sprite = pygame.image.load('./assets/enemymedium.png')
            self.middle = (7, 9)
            self.speed = 0.4
            self.max_health = 40
            self.damage = 10
            self.reward = 20
            
        elif self.type == "heavy":
            self.sprite = pygame.image.load('./assets/enemyheavy.png')
            self.middle = (7, 10)
            self.speed = 0.3
            self.max_health = 80
            self.damage = 20
            self.reward = 40

        self.health = self.max_health

        self.to_reward = False

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
        #If enemy x coord has not reached its destination x coord
        if round(self.current_pos[0]) != round(self.dest_pos[0]):
            self.current_pos[0] += self.move_vector[0]

        #If enemy y coord has not reached its destination y coord
        if round(self.current_pos[1]) != round(self.dest_pos[1]):
            self.current_pos[1] += self.move_vector[1]

        #If enemy has reached its destination in a movement
        elif round(self.current_pos[1]) == round(self.dest_pos[1]) and round(self.current_pos[0]) == round(self.dest_pos[0]):
            #Current tile is updated
            self.current_tile = self.dest_tile
            #If the end tile has been reached, enemy dies without giving a reward and player loses HP
            if self.current_tile == self.end_tile:
                self.damaging = True
                self.alive = False
            else:
                self.moved = True

        #If the enemy is on fire (fire_damage is not 0)
        if self.fire_damage:
            self.on_fire_timer += 1
            #Every second (60 frames) the enemy loses some health
            if self.on_fire_timer % 60 == 0:
                self.health -= self.fire_damage
            #After 10 seconds enemy is no longer on fire
            if self.on_fire_timer == 600:
                self.fire_damage = 0
                self.on_fire_timer = 0
        
        #If the enemy's health reaches 0 it is dead and its death reward is given to the player
        if self.health <= 0:
            self.to_reward = True
            self.alive = False
        
        #Enemy sprite is blitted onto the scene
        blit_pos = (self.current_pos[0] - self.middle[0], self.current_pos[1] - self.middle[1])
        self.game["display"].blit(self.sprite_rot, blit_pos)

    
    def update_health_bar(self):
        #The position of the health bar is calculated from the enemy's position
        red_rect = (self.current_pos[0] - 7.5, self.current_pos[1] - 15, 15, 2)
        #The green rectangle's width is calculated based on the enemy's remaining HP
        green_rect = (self.current_pos[0] - 7.5, self.current_pos[1] - 15, 15 * (self.health / self.max_health), 2)

        pygame.draw.rect(self.game["display"], (197, 9, 9), red_rect)
        #If the enemy is on fire, green rectangle has its colour changed to orange
        if self.fire_damage:
            pygame.draw.rect(self.game["display"], (255, 150, 9), green_rect)
        else:
            pygame.draw.rect(self.game["display"], (9, 197, 9), green_rect)
