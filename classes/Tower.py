import pygame
from .GridTile import GridTile

class Tower(GridTile):

    def set_type(self, type):
        self.type = type

        #Depending on what type the tower is, corresponding assets are loaded
        if self.type == "basic":
            self.sprite = pygame.image.load("./assets/towerbasic.png")
            self.range = 125
            self.damage = 5

        elif self.type == "splash":
            self.sprite = pygame.image.load("./assets/towersplash.png")
            self.range = 75
            self.damage = 2

        elif self.type == "sniper":
            self.sprite = pygame.image.load("./assets/towersniper.png")
            self.range = 250
            self.damage = 5

        elif self.type == "incendiary":
            self.sprite = pygame.image.load("./assets/towerincendiary.png")
            self.range = 100
            self.damage = 1


    def update(self, mouse_tile, enemies):
        #Blits tower sprite
        self.game["display"].blit(self.sprite, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))
        #Draws transparent square on top if tile is hovered over
        if tuple(mouse_tile) == self.pos:
            self.game["display"].blit(self.hover_square, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))

        nearby_enemies = []
        for enemy in enemies:
            if enemy.alive:
                #Calculates the distance of each live enemy from the tower using pythagoras
                distance_away = (((self.pos[0]*50 + 460) - enemy.current_pos[0])**2 + ((self.pos[1]*50 + 140) - enemy.current_pos[1])**2)**0.5
                #If the enemy is within the tower's range
                if distance_away < self.range:
                    nearby_enemies.append((enemy, distance_away))

        #If array is not empty
        if nearby_enemies:
            #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
            nearest_enemy = sorted(nearby_enemies, key=lambda x: x[1])[0][0]

