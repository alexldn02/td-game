import pygame

class Button:

    def __init__(self, game, type):
        self.game = game

        self.set_type(type)


    def get_type(self):
        return self.type

    
    def set_type(self, type):
        self.type = type

        #Bounds and sprites are set depending on what type of button is instantiated
        if self.type == "back":
            self.bounds = [[1105, 1270], [10, 60]]
            self.sprite = pygame.image.load("./assets/backbtn.png")
            self.sprite_hovered = pygame.image.load("./assets/backbtnhovered.png")

        elif self.type == "createbasic":
            self.bounds = [[35, 345], [115, 225]]
            self.sprite = pygame.image.load("./assets/createbasicbtn.png")
            self.sprite_hovered = pygame.image.load("./assets/createbasicbtnhovered.png")
            self.sprite_selected = pygame.image.load("./assets/createbasicbtnselected.png")

        elif self.type == "createsplash":
            self.bounds = [[35, 345], [245, 355]]
            self.sprite = pygame.image.load("./assets/createsplashbtn.png")
            self.sprite_hovered = pygame.image.load("./assets/createsplashbtnhovered.png")
            self.sprite_selected = pygame.image.load("./assets/createsplashbtnselected.png")

        elif self.type == "createsniper":
            self.bounds = [[35, 345], [375, 485]]
            self.sprite = pygame.image.load("./assets/createsniperbtn.png")
            self.sprite_hovered = pygame.image.load("./assets/createsniperbtnhovered.png")
            self.sprite_selected = pygame.image.load("./assets/createsniperbtnselected.png")

        elif self.type == "createincendiary":
            self.bounds = [[35, 345], [505, 615]]
            self.sprite = pygame.image.load("./assets/createincendiarybtn.png")
            self.sprite_hovered = pygame.image.load("./assets/createincendiarybtnhovered.png")
            self.sprite_selected = pygame.image.load("./assets/createincendiarybtnselected.png")

        elif self.type == "nextwavelight":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwavelightbtn.png")
            self.sprite_hovered = pygame.image.load("./assets/nextwavelightbtnhovered.png")

        elif self.type == "nextwavemedium":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwavemediumbtn.png")
            self.sprite_hovered = pygame.image.load("./assets/nextwavemediumbtnhovered.png")

        elif self.type == "nextwaveheavy":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwaveheavybtn.png")
            self.sprite_hovered = pygame.image.load("./assets/nextwaveheavybtnhovered.png")

        elif self.type == "wavesend":
            self.bounds = [[35, 345], [775, 925]]
            self.sprite = pygame.image.load("./assets/nextwaveheavybtnhovered.png")
            self.sprite_hovered = pygame.image.load("./assets/nextwaveheavybtn.png")

    def within_bounds(self, mouse_pos):
        #Returns true if mouse is over button
        if mouse_pos[0] >= self.bounds[0][0] and mouse_pos[0] < self.bounds[0][1] and mouse_pos[1] >= self.bounds[1][0] and mouse_pos[1] < self.bounds[1][1]:
            return True
        else:
            return False


    def update(self, mouse_pos, selected = ""):
        #Blits sprite depending on whether button is selected or hovered over
        if selected == self.type:
            self.game["display"].blit(self.sprite_selected, (self.bounds[0][0], self.bounds[1][0]))
        elif self.within_bounds(mouse_pos):
            self.game["display"].blit(self.sprite_hovered, (self.bounds[0][0], self.bounds[1][0]))
        else:
            self.game["display"].blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))
