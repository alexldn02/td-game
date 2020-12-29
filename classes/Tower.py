import pygame
import random
import math
from .GridTile import GridTile

class Tower(GridTile):

    def __init__(self, surface, type, pos):
        
        #Calls GridTile constructor
        super().__init__(surface, type, pos)

        self.selected_square = pygame.Surface((50, 50))
        self.selected_square.set_alpha(64)
        self.selected_square.fill((255,255,255))

        self.attack_wait_time = 0
        self.firing = False

        self.agro = False
        self.target = None

        self.level = 1

        self.upgrade_cost = 50

        self.font = pygame.font.Font("./assets/font.ttf", 16)


    def set_type(self, type):
        self.type = type

        #Depending on what type the tower is, corresponding assets are loaded and stats are set
        if self.type == "basic":
            self.sprite = pygame.image.load("./assets/towerbasic.png")
            self.sprite_agro = pygame.image.load("./assets/towerbasicagro.png")
            self.range = 125
            self.damage = 4
            self.fire_rate = 0.75

        elif self.type == "splash":
            self.sprite = pygame.image.load("./assets/towersplash.png")
            self.sprite_agro = pygame.image.load("./assets/towersplashagro.png")
            self.range = 100
            self.damage = 2
            self.fire_rate = 1.5

        elif self.type == "sniper":
            self.sprite = pygame.image.load("./assets/towersniper.png")
            self.sprite_agro = pygame.image.load("./assets/towersniperagro.png")
            self.range = 200
            self.damage = 8
            self.fire_rate = 1.5

        elif self.type == "flame":
            self.sprite = pygame.image.load("./assets/towerflame.png")
            self.sprite_agro = pygame.image.load("./assets/towerflameagro.png")
            self.range = 125
            self.damage = 2
            self.fire_damage = 1
            self.fire_rate = 1


    def level_up(self):
        #Improves stats for the tower

        self.level += 1

        self.upgrade_cost += 10

        self.range = self.range * 1.05

        self.fire_rate = self.fire_rate * 0.95
        
        if self.type == "flame":
            self.fire_damage = self.fire_damage * 1.05
        else:
            self.damage = self.damage * 1.05


    def basic_attack(self, enemies):
        #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
        self.sort_enemies(enemies)
        #Selects only the enemy object, discarding its distance from the tower
        nearest_enemy = enemies[0][0]

        if not self.target:
            self.target = nearest_enemy
        elif not self.target.alive:
            self.target = None
            self.firing = False

        if self.target:
            self.attack_wait_time += 1
            
            if self.attack_wait_time == 5:
                self.firing = False
                
            if self.attack_wait_time >= math.floor(60 * self.fire_rate):
                self.target.health -= self.damage
                self.firing = True
                self.attack_wait_time = 0


    def splash_attack(self, enemies):
        self.attack_wait_time += 1

        if self.attack_wait_time >= math.floor(60 * self.fire_rate):
            for enemy in enemies:
                enemy[0].health -= self.damage
            self.attack_wait_time = 0


    def sniper_attack(self, enemies):
        #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
        self.sort_enemies(enemies)
        #Selects only the enemy object, discarding its distance from the tower
        nearest_enemy = enemies[0][0]

        if not self.target:
            self.target = nearest_enemy
        elif not self.target.alive:
            self.target = None
            self.firing = False

        if self.target:
            self.attack_wait_time += 1
            
            if self.attack_wait_time == 2:
                self.firing = False
                
            if self.attack_wait_time >= math.floor(60 * self.fire_rate):
                self.target.health -= self.damage
                self.firing = True
                self.attack_wait_time = 0


    def flame_attack(self, enemies):
        #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
        self.sort_enemies(enemies)

        nearest_on_fire = True
        i = 0
        while nearest_on_fire:
            if i < len(enemies):
                #Selects only the enemy object, discarding its distance from the tower
                nearest_enemy = enemies[i][0]
                i += 1
                
                if not nearest_enemy.fire_damage:
                    nearest_on_fire = False
            else:
                nearest_enemy = enemies[0][0]
                nearest_on_fire = False

        if not self.target:
            self.target = nearest_enemy
        elif not self.target.alive:
            self.target = None
            self.firing = False
                
        if self.target:
            self.attack_wait_time += 1

            if self.attack_wait_time == 20:
                self.firing = False
                self.target = None

            if self.attack_wait_time >= math.floor(60 * self.fire_rate):
                self.target.health -= self.damage
                self.target.fire_damage = self.fire_damage
                self.firing = True
                self.attack_wait_time = 0

    
    def sort_enemies(self, enemies):
        #Merge sort algorithm to order enemies by distance from the tower

        if len(enemies) > 1:
            #The list is split down the middle, separating both halves
            middle = len(enemies) // 2
            left_half = enemies[:middle]
            right_half = enemies[middle:]

            #Recursively sorts both halves by splitting them and merging them
            self.sort_enemies(left_half)
            self.sort_enemies(right_half)

            #Index of the left half list
            l = 0
            #Index of the right half list
            r = 0
            #Index of the merged list
            m = 0

            #Loop ends after one half is fully checked
            while l < len(left_half) and r < len(right_half):
                #Closest of the two left and right half enemies is appended to the merged list
                #Then moves on to the next enemy in that half to be compared to the further enemy
                if left_half[l][1] < right_half[r][1]:
                    enemies[m] = left_half[l]
                    l += 1
                else:
                    enemies[m] = right_half[r]
                    r += 1
                m += 1

            #Right half is fully checked but not left
            while l < len(left_half):
                #Appends all remaining enemies in left half to the merged list
                enemies[m] = left_half[l]
                l += 1
                m += 1
            
            #Left half is fully checked but not right
            while r < len(right_half):
                #Appends all remaining enemies in right half to the merged list
                enemies[m] = right_half[r]
                r += 1
                m += 1


    def update(self, mouse_tile, selected, enemies):
        #Blits appropriate tower sprite
        if self.agro:
            self.surface.blit(self.sprite_agro, (self.pos[0]*50, self.pos[1]*50))
        else:
            self.surface.blit(self.sprite, (self.pos[0]*50, self.pos[1]*50))

        level_text = self.font.render(str(self.level), True, (255,255,255))
        self.surface.blit(level_text, (self.pos[0]*50, self.pos[1]*50))

        if selected == self.pos:
            self.surface.blit(self.selected_square, (self.pos[0]*50, self.pos[1]*50))
        #Draws transparent square on top if tile is hovered over
        elif tuple(mouse_tile) == self.pos:
            self.surface.blit(self.hover_square, (self.pos[0]*50, self.pos[1]*50))

        nearby_enemies = []
        for enemy in enemies:
            if enemy.alive:
                #Calculates the distance of each live enemy from the tower using pythagoras
                distance_away = (((self.pos[0]*50 + 25) - enemy.current_pos[0])**2 + ((self.pos[1]*50 + 25) - enemy.current_pos[1])**2)**0.5
                #If the enemy is within the tower's range
                if distance_away < self.range:
                    #The enemy is added to the nearby enemies array
                    nearby_enemies.append((enemy, distance_away))

        #If nearby enemies array is not empty, meaning there are enemies within range of tower
        if nearby_enemies:
            #Tower is set to agro mode so sprite is changed
            self.agro = True

            #Attack style dependent on tower type
            if self.type == "basic":
                self.basic_attack(nearby_enemies)
            elif self.type == "splash":
                self.splash_attack(nearby_enemies)
            elif self.type == "sniper":
                self.sniper_attack(nearby_enemies)
            else:
                self.flame_attack(nearby_enemies)
        
        #If there are no enemies nearby, tower is not agro
        else:
            self.agro = False
            self.target = None


    def update_attack_anim(self):
        middle_pos = (self.pos[0]*50 + 25, self.pos[1]*50 + 25)
        if self.firing and self.target:
            if self.type == "basic":
                pygame.draw.line(self.surface, (255,255,255), middle_pos, tuple(self.target.current_pos), 2)
            elif self.type == "sniper":
                pygame.draw.line(self.surface, (255,255,255), middle_pos, tuple(self.target.current_pos))
            elif self.type == "flame":
                pygame.draw.line(self.surface, (255,100,0), middle_pos, tuple(self.target.current_pos), 3)

        #The splash attack animation is much more complicated than the others
        elif self.type == "splash":
            max_radius = math.floor(self.range)

            #Radius of circle is determined by the wait time between attacks so it gets bigger and then starts small again next attack
            radius = math.floor(max_radius * math.sin(self.attack_wait_time/90 * 0.5*math.pi))

            #Margins refer to the distance between the middle of the tower and the edges of the grid
            x_margins = (middle_pos[0], 800 - middle_pos[0])
            y_margins = (middle_pos[1], 800 - middle_pos[1])

            #Margins are used to calculate how much of the Surface rect needs to be cut off to stop the attack animation from going out of the grid
            #Range is used so that the Surface rect is as small as possible to keep the fps up
            if max_radius > x_margins[0]:
                x_cutoff_left = max_radius - x_margins[0]
            else:
                x_cutoff_left = 0
            if max_radius > x_margins[1]:
                x_cutoff_right = max_radius - x_margins[1]
            else:
                x_cutoff_right = 0

            if max_radius > y_margins[0]:
                y_cutoff_top = max_radius - y_margins[0]
            else:
                y_cutoff_top = 0
            if max_radius > y_margins[1]:
                y_cutoff_bottom = max_radius - y_margins[1]
            else:
                y_cutoff_bottom = 0

            #Width and height of the invisible Surface rectangle
            surface_dimensions = (max_radius*2 - x_cutoff_left - x_cutoff_right, max_radius*2 - y_cutoff_top - y_cutoff_bottom)

            surface_pos = (self.pos[0]*50 + 25 - max_radius + x_cutoff_left, self.pos[1]*50 + 25 - max_radius + y_cutoff_top)

            #The Surface object has to be used because pygame cannot draw transparent circles unless they are blitted as part of a transparent Surface
            #pygame.draw.circle() cannot have an alpha value
            surface = pygame.Surface(surface_dimensions)
            surface.set_colorkey((0,0,0))

            #Alpha value decreases with time from the beginning of the attack to have a fade-out effect
            surface.set_alpha(192 - 192 * math.sin(self.attack_wait_time/90 * 0.5*math.pi))

            #White circle is drawn onto the Surface
            pygame.draw.circle(surface, (255,255,255), (max_radius - x_cutoff_left, max_radius - y_cutoff_top), radius)

            #Surface object is blitted to the grid surface
            self.surface.blit(surface, surface_pos)
