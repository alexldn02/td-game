import pygame

class Button:

    def __init__(self, game, type):
        self.game = game

        self.stats_font = pygame.font.Font("./assets/font.ttf", 16)
        self.time_left_font = pygame.font.Font("./assets/font.ttf", 25)
        self.enemy_count_font = pygame.font.Font("./assets/font.ttf", 25)

        self.set_type(type)

        size = (self.bounds[0][1] - self.bounds[0][0], self.bounds[1][1] - self.bounds[1][0])

        self.hover_rect = pygame.Surface(size)
        self.hover_rect.set_alpha(32)
        self.hover_rect.fill((255,255,255))

        self.selected_rect = pygame.Surface(size)
        self.selected_rect.set_alpha(64)
        self.selected_rect.fill((255,255,255))

        self.disabled_rect = pygame.Surface(size)
        self.disabled_rect.set_alpha(64)
        self.disabled_rect.fill((0,0,0))

        self.damage_icon = pygame.image.load("./assets/icondamage.png")
        self.fire_rate_icon = pygame.image.load("./assets/iconfirerate.png")
        self.range_icon = pygame.image.load("./assets/iconrange.png")
        self.fire_damage_icon = pygame.image.load("./assets/iconfiredamage.png")

    
    def set_type(self, type):
        self.type = type

        #Bounds and sprites are set depending on what type of button is instantiated
        if self.type == "back":
            self.bounds = [[1105, 1270], [10, 60]]
            self.sprite = pygame.image.load("./assets/backbtn.png")

        elif self.type == "createbasic":
            self.bounds = [[35, 345], [115, 225]]
            self.sprite = pygame.image.load("./assets/createbasicbtn.png")

        elif self.type == "createsplash":
            self.bounds = [[35, 345], [245, 355]]
            self.sprite = pygame.image.load("./assets/createsplashbtn.png")

        elif self.type == "createsniper":
            self.bounds = [[35, 345], [375, 485]]
            self.sprite = pygame.image.load("./assets/createsniperbtn.png")

        elif self.type == "createflame":
            self.bounds = [[35, 345], [505, 615]]
            self.sprite = pygame.image.load("./assets/createflamebtn.png")

        elif self.type == "upgradetower":
            self.bounds = [[35, 235], [635, 745]]
            self.sprite = pygame.image.load("./assets/upgradetowerbtn.png")

        elif self.type == "deletetower":
            self.bounds = [[255, 345], [635, 745]]
            self.sprite = pygame.image.load("./assets/deletetowerbtn.png")

        elif self.type == "nextwavelight":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwavelightbtn.png")

        elif self.type == "nextwavemedium":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwavemediumbtn.png")

        elif self.type == "nextwaveheavy":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwaveheavybtn.png")

        elif self.type == "wavesend":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwavenonebtn.png")


    def within_bounds(self, mouse_pos):
        #Returns true if mouse is over button
        if mouse_pos[0] >= self.bounds[0][0] and mouse_pos[0] < self.bounds[0][1] and mouse_pos[1] >= self.bounds[1][0] and mouse_pos[1] < self.bounds[1][1]:
            return True
        else:
            return False


    def update(self, mouse_pos, selected, count = -1):
        #Blits sprite
        self.game["display"].blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        #Blits text if next wave
        #if self.type == "nextwavelight" or self.type == "nextwavemedium" or self.type == "nextwaveheavy":            

        if self.type == "nextwavelight" or self.type == "nextwavemedium" or self.type == "nextwaveheavy":
            #time_left_text = self.time_left_font.render(str(time_left), True, (115,113,102))
            #self.game["display"].blit(time_left_text, (96, 839))

            enemy_count_text = self.enemy_count_font.render(str(count), True, (0,0,0))

            if len(str(count)) == 1:
                self.game["display"].blit(enemy_count_text, (265, 875))
            else:
                self.game["display"].blit(enemy_count_text, (260, 875))

        #Blits selected transparent rectangle if selected
        if selected == self.type:
            self.game["display"].blit(self.selected_rect, (self.bounds[0][0], self.bounds[1][0]))
        #Or disabled transparent rectangle if button is disabled
        elif (self.type == "upgradetower" or self.type == "deletetower") and type(selected) != tuple or self.type == "wavesend":
            self.game["display"].blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))
        #Or hovered transparent rectangle if hovered over and not selected or disabled
        elif self.within_bounds(mouse_pos):
            self.game["display"].blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))


            
