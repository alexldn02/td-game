import pygame
from .Button import Button

class UpgradeButton(Button):
    def __init__(self, game):
        self.game = game

        self.stats_font = pygame.font.Font("./assets/font.ttf", 16)

        self.bounds = [[35, 235], [635, 745]]

        self.sprite = pygame.image.load("./assets/upgradetowerbtn.png")

        size = (self.bounds[0][1] - self.bounds[0][0], self.bounds[1][1] - self.bounds[1][0])

        self.hover_rect = pygame.Surface(size)
        self.hover_rect.set_alpha(32)
        self.hover_rect.fill((255,255,255))

        self.disabled_rect = pygame.Surface(size)
        self.disabled_rect.set_alpha(64)
        self.disabled_rect.fill((0,0,0))

        self.damage_icon = pygame.image.load("./assets/icondamage.png")
        self.fire_rate_icon = pygame.image.load("./assets/iconfirerate.png")
        self.range_icon = pygame.image.load("./assets/iconrange.png")
        self.fire_damage_icon = pygame.image.load("./assets/iconfiredamage.png")


    def update(self, mouse_pos, selected, money):
        #Blits sprite
        self.game["display"].blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        if not (selected == None or type(selected) == str) and selected.level < 10:

            level_text = self.stats_font.render("Lvl. " + str(selected.level+1), True, (9, 197, 9))
            self.game["display"].blit(level_text, (112, 684))

            if selected.type == "flame":
                self.game["display"].blit(self.fire_damage_icon, (110, 705))
                fire_damage_text = self.stats_font.render(str(round(selected.fire_damage*1.05, 2)), True, (9, 197, 9))
                self.game["display"].blit(fire_damage_text, (130, 707))
            else:
                self.game["display"].blit(self.damage_icon, (110, 705))
                damage_text = self.stats_font.render(str(round(selected.damage*1.05, 2)), True, (9, 197, 9))
                self.game["display"].blit(damage_text, (130, 707))

            self.game["display"].blit(self.fire_rate_icon, (164, 682))
            fire_rate_text = self.stats_font.render(str(round(selected.fire_rate*0.95, 2)), True, (9, 197, 9))
            self.game["display"].blit(fire_rate_text, (184, 684))

            self.game["display"].blit(self.range_icon, (164, 705))
            range_text = self.stats_font.render(str(int(round(selected.range*1.1, 0))), True, (9, 197, 9))
            self.game["display"].blit(range_text, (184, 707))

        #Disabled transparent rectangle if button is disabled
        if selected == None or selected.level == 10 or money < 50:
            self.game["display"].blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))
        
        #Or hovered transparent rectangle if hovered over and not selected or disabled
        elif self.within_bounds(mouse_pos):
            self.game["display"].blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))