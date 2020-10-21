import pygame
import random
import math
from .GridTile import GridTile

class Tower(GridTile):

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
            self.fire_rate = 1

        elif self.type == "sniper":
            self.sprite = pygame.image.load("./assets/towersniper.png")
            self.sprite_agro = pygame.image.load("./assets/towersniperagro.png")
            self.range = 200
            self.damage = 6
            self.fire_rate = 1.5

        elif self.type == "incendiary":
            self.sprite = pygame.image.load("./assets/towerincendiary.png")
            self.sprite_agro = pygame.image.load("./assets/towerincendiaryagro.png")
            self.range = 125
            self.damage = 2
            self.fire_damage = 1
            self.fire_rate = 1


    def level_up(self):

        self.level += 1

        self.range = self.range * 1.05

        self.fire_rate = self.fire_rate * 0.95
        
        if self.type == "incendiary":
            self.fire_damage = self.fire_damage * 1.05
        else:
            self.damage = self.damage * 1.05


    def basic_attack(self, enemies):
        #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
        self.sort(enemies)
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
                
            if self.attack_wait_time == math.floor(60 * self.fire_rate):
                self.target.health -= self.damage
                self.firing = True
                self.attack_wait_time = 0


    def splash_attack(self, enemies):
        self.attack_wait_time += 1
        if self.attack_wait_time == math.floor(60 * self.fire_rate):
            for enemy in enemies:
                enemy[0].health -= self.damage  
            self.attack_wait_time = 0


    def sniper_attack(self, enemies):
        #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
        self.sort(enemies)
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
                
            if self.attack_wait_time == math.floor(60 * self.fire_rate):
                self.target.health -= self.damage
                self.firing = True
                self.attack_wait_time = 0


    def incendiary_attack(self, enemies):
        #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
        self.sort(enemies)
        #Selects only the enemy object, discarding its distance from the tower
        nearest_enemy = enemies[0][0]

        if not self.target:
            self.target = nearest_enemy
        elif not self.target.alive:
            self.target = None
            self.firing = False
                
        if self.target:
            self.attack_wait_time += 1
            print(math.floor(60 * self.fire_rate))

            if self.attack_wait_time == 20:
                self.firing = False
                self.target = None

            if self.attack_wait_time == math.floor(60 * self.fire_rate):
                self.target.health -= self.damage
                self.target.fire_damage = self.fire_damage
                self.firing = True
                self.attack_wait_time = 0

    
    def sort(self, enemies):
        #Merge sort algorithm to order enemies by distance from the tower

        #List only needs to be sorted if it has more than 1 item
        if len(enemies) > 1:
            mid = len(enemies) // 2
            left_half = enemies[:mid]
            right_half = enemies[mid:]
            self.sort(left_half)
            self.sort(right_half)
            a = 0
            b = 0
            c = 0

            while a < len(left_half) and b < len(right_half):
                if left_half[a][1] < right_half[b][1]:
                    enemies[c] = left_half[a]
                    a += 1
                else:
                    enemies[c] = right_half[b]
                    b += 1
                c += 1

            while a < len(left_half):
                enemies[c] = left_half[a]
                a += 1
                c += 1
            
            while b < len(right_half):
                enemies[c] = right_half[b]
                b += 1
                c += 1


    def update(self, mouse_tile, selected, enemies):
        #Blits appropriate tower sprite
        if self.agro:
            self.game["display"].blit(self.sprite_agro, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))
        else:
            self.game["display"].blit(self.sprite, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))

        level_text = self.font.render(str(self.level), True, (255,255,255))
        self.game["display"].blit(level_text, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))

        if selected == self.pos:
            self.game["display"].blit(self.selected_square, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))
        #Draws transparent square on top if tile is hovered over
        elif tuple(mouse_tile) == self.pos:
            self.game["display"].blit(self.hover_square, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))

        nearby_enemies = []
        for enemy in enemies:
            if enemy.alive:
                #Calculates the distance of each live enemy from the tower using pythagoras
                distance_away = (((self.pos[0]*50 + 460) - enemy.current_pos[0])**2 + ((self.pos[1]*50 + 140) - enemy.current_pos[1])**2)**0.5
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
                self.incendiary_attack(nearby_enemies)
        
        #If there are no enemies nearby, tower is not agro
        else:
            self.agro = False
            self.target = None


    def update_attack_anim(self):
        middle_pos = (self.pos[0]*50 + 460, self.pos[1]*50 + 140)
        if self.firing and self.target:
            if self.type == "basic":
                pygame.draw.line(self.game["display"], (255,255,255), middle_pos, tuple(self.target.current_pos), 2)
            elif self.type == "sniper":
                pygame.draw.line(self.game["display"], (255,255,255), middle_pos, tuple(self.target.current_pos))
            elif self.type == "incendiary":
                pygame.draw.line(self.game["display"], (255,100,0), middle_pos, tuple(self.target.current_pos), 3)
        elif self.type == "splash":
            max_radius = math.floor(self.range)

            #Radius of circle is determined by the wait time between attacks so it gets bigger and then starts small again next attack
            radius = math.floor(max_radius * math.sin(self.attack_wait_time/60 * 0.5*math.pi))

            #Margins refer to the distance between the middle of the tower and the edges of the grid
            x_margins = (middle_pos[0] - 435, 1235 - middle_pos[0])
            y_margins = (middle_pos[1] - 115, 915 - middle_pos[1])

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

            #The Surface object has to be used because pygame cannot draw transparent circles unless they are blitted as part of a transparent Surface
            #pygame.draw.circle() cannot have an alpha value
            surface = pygame.Surface(surface_dimensions)
            surface.set_colorkey((0,0,0))

            #Alpha value decreases with time from the beginning of the attack to have a fade-out effect
            surface.set_alpha(192 - 192 * math.sin(self.attack_wait_time/60 * 0.5*math.pi))

            #White circle is drawn onto the Surface
            pygame.draw.circle(surface, (255,255,255), (max_radius - x_cutoff_left, max_radius - y_cutoff_top), radius)

            surface_pos = (self.pos[0]*50 + 460 - max_radius + x_cutoff_left, self.pos[1]*50 + 140 - max_radius + y_cutoff_top)

            #Surface object is blitted to the scene
            self.game["display"].blit(surface, surface_pos)