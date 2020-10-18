import pygame
from .GridTile import GridTile

class Tower(GridTile):

    def set_type(self, type, level = 0):
        self.type = type

        #Depending on what type the tower is, corresponding assets are loaded and stats are set
        if self.type == "basic":
            self.sprite = pygame.image.load("./assets/towerbasic.png")
            self.sprite_agro = pygame.image.load("./assets/towerbasicagro.png")
            self.range = 125
            self.damage = 5
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
            self.damage = 7
            self.fire_rate = 1.5

        elif self.type == "incendiary":
            self.sprite = pygame.image.load("./assets/towerincendiary.png")
            self.sprite_agro = pygame.image.load("./assets/towerincendiaryagro.png")
            self.range = 125
            self.damage = 2
            self.fire_damage = 1
            self.fire_rate = 1


    def basic_attack(self, enemy):
        self.attack_wait_time += 1
        if self.attack_wait_time == 60 * self.fire_rate:
            enemy.health -= self.damage    
            self.attack_wait_time = 0


    def splash_attack(self, enemies):
        self.attack_wait_time += 1
        if self.attack_wait_time == 60 * self.fire_rate:
            for enemy in enemies:
                enemy[0].health -= self.damage  
            self.attack_wait_time = 0


    def sniper_attack(self, enemy):
        self.attack_wait_time += 1
        if self.attack_wait_time == 60 * self.fire_rate:
            enemy.health -= self.damage 
            self.attack_wait_time = 0


    def incendiary_attack(self, enemy):
        self.attack_wait_time += 1
        if self.attack_wait_time == 60 * self.fire_rate:
            enemy.health -= self.damage
            enemy.fire_damage = self.fire_damage
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


    def update(self, mouse_tile, enemies):
        #Blits appropriate tower sprite
        if self.agro:
            self.game["display"].blit(self.sprite_agro, (self.pos[0]*50 + 435, self.pos[1]*50 + 115))
        else:
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
                    #The enemy is added to the nearby enemies array
                    nearby_enemies.append((enemy, distance_away))

        #If nearby enemies array is not empty, meaning there are enemies within range of tower
        if nearby_enemies:
            #Tower is set to agro mode so sprite is changed
            self.agro = True

            #Nearest enemy is the first of the list where it is sorted by the distance away from tower of each enemy nearby
            self.sort(nearby_enemies)
            #Selects only the enemy object, discarding its distance from the tower
            nearest_enemy = nearby_enemies[0][0]

            #Nearest enemy is attacked using attack style dependent on tower type
            if self.type == "basic":
                self.basic_attack(nearest_enemy)
            elif self.type == "splash":
                self.splash_attack(nearby_enemies)
            elif self.type == "sniper":
                self.sniper_attack(nearest_enemy)
            else:
                self.incendiary_attack(nearest_enemy)
        
        #If there are no enemies nearby, tower is not agro
        else:
            self.agro = False

            


