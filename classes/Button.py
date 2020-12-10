import pygame

class Button:

    def __init__(self, surface, type):
        self.surface = surface

        self.set_type(type)

        size = (self.bounds[0][1] - self.bounds[0][0], self.bounds[1][1] - self.bounds[1][0])

        self.hover_rect = pygame.Surface(size)
        self.hover_rect.set_alpha(32)
        self.hover_rect.fill((255,255,255))

        self.disabled_rect = pygame.Surface(size)
        self.disabled_rect.set_alpha(64)
        self.disabled_rect.fill((0,0,0))

    
    def set_type(self, type):
        self.type = type

        #Bounds and sprites are set depending on what type of button is instantiated
        if self.type == "back":
            self.bounds = [[1105, 1265], [10, 60]]
            self.sprite = pygame.image.load("./assets/backbtn.png")

        elif self.type == "retry":
            self.bounds = [[935, 1095], [10, 60]]
            self.sprite = pygame.image.load("./assets/retrybtn.png")

        elif self.type == "deletetower":
            self.bounds = [[255, 345], [635, 745]]
            self.sprite = pygame.image.load("./assets/deletetowerbtn.png")

        elif self.type == "play":
            self.bounds = [[175, 415], [665, 775]]
            self.sprite = pygame.image.load("./assets/playbtn.png")

        elif self.type == "exit":
            self.bounds = [[175, 415], [800, 910]]
            self.sprite = pygame.image.load("./assets/exitbtn.png")
        
        elif self.type == "return":
            self.bounds = [[450, 630], [585, 645]]
            self.sprite = pygame.image.load("./assets/returnbtn.png")

        elif self.type == "levelendretry":
            self.bounds = [[650, 830], [585, 645]]
            self.sprite = pygame.image.load("./assets/levelendretrybtn.png")


    def within_bounds(self, mouse_pos):
        #Returns true if mouse is over button
        if mouse_pos[0] >= self.bounds[0][0] and mouse_pos[0] < self.bounds[0][1] and mouse_pos[1] >= self.bounds[1][0] and mouse_pos[1] < self.bounds[1][1]:
            return True
        else:
            return False


    def update(self, mouse_pos, selected = None):
        #Blits sprite
        self.surface.blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        #And disabled transparent rectangle if button is disabled
        if self.type == "deletetower" and (selected == None or type(selected) == str):
            self.surface.blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))
            
        #Or hovered transparent rectangle if hovered over and not disabled
        elif self.within_bounds(mouse_pos):
            self.surface.blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))