import pygame
import random
import math

class Enemy:

    def __init__(self, game, type, start_tile, end_tile):
        self.game = game        

        self.type = type
        self.current_tile = start_tile

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
        self.dest_pos = self.current_pos

        self.sprite_rot = pygame.transform.rotate(self.sprite, 0)

    def move_to(self, dest_tile):
        self.dest_pos = (dest_tile[0]*50 + random.randint(5, 45) + 435, dest_tile[1]*50 + random.randint(5, 45) + 115)

        self.move_distance = ((self.dest_pos[0] - self.current_pos[0])**2 + (self.dest_pos[1] - self.current_pos[1])**2)**0.5

        self.move_vector = (self.speed * ((self.dest_pos[0] - self.current_pos[0]) / self.move_distance), self.speed * ((self.dest_pos[1] - self.current_pos[1]) / self.move_distance))

        radians = math.atan2(self.dest_pos[1] - self.current_pos[1], self.dest_pos[0] - self.current_pos[0])
        self.move_angle = 270 - math.degrees(radians)
        
        self.sprite_rot = pygame.transform.rotate(self.sprite, self.move_angle)

    def update(self):
        if round(self.current_pos[0]) != round(self.dest_pos[0]):
            self.current_pos[0] += self.move_vector[0]
            
        if round(self.current_pos[1]) != round(self.dest_pos[1]):
            self.current_pos[1] += self.move_vector[1]
        elif round(self.current_pos[0]) == round(self.dest_pos[0]):
            self.current_pos = self.dest_pos
        
        blit_pos = (self.current_pos[0] - self.middle[0], self.current_pos[1] - self.middle[1])
        self.game["display"].blit(self.sprite_rot, blit_pos)
