import pygame
from .Button import Button

class UpgradeButton(Button):
    def __init__(self, surface):
        self.bounds = [[35, 235], [635, 745]]

        self.sprite = pygame.image.load("./assets/upgradetowerbtn.png")

        super().__init__(surface, "")
        
        self.stats_font = pygame.font.Font("./assets/font.ttf", 16)
        self.cost_font = pygame.font.Font("./assets/font.ttf", 24)

        self.money_icon = pygame.image.load("./assets/iconmoney.png")
        self.damage_icon = pygame.image.load("./assets/icondamage.png")
        self.fire_rate_icon = pygame.image.load("./assets/iconfirerate.png")
        self.range_icon = pygame.image.load("./assets/iconrange.png")
        self.fire_damage_icon = pygame.image.load("./assets/iconfiredamage.png")


    def update(self, mouse_pos, tower, money):
        #Blits sprite
        self.surface.blit(self.sprite, (self.bounds[0][0], self.bounds[1][0]))

        if not (tower == None) and tower.level < 10:

            self.surface.blit(self.money_icon, (135, 647))
            cost_text = self.cost_font.render(str(tower.upgrade_cost), True, (54, 67, 63))
            self.surface.blit(cost_text, (155, 647))

            level_text = self.stats_font.render("Lvl. " + str(tower.level+1), True, (9, 197, 9))
            self.surface.blit(level_text, (112, 684))

            if tower.type == "flame":
                self.surface.blit(self.fire_damage_icon, (110, 705))
                fire_damage_text = self.stats_font.render(str(round(tower.fire_damage*1.05, 2)), True, (9, 197, 9))
                self.surface.blit(fire_damage_text, (130, 707))
            else:
                self.surface.blit(self.damage_icon, (110, 705))
                damage_text = self.stats_font.render(str(round(tower.damage*1.05, 2)), True, (9, 197, 9))
                self.surface.blit(damage_text, (130, 707))

            self.surface.blit(self.fire_rate_icon, (164, 682))
            fire_rate_text = self.stats_font.render(str(round(tower.fire_rate*0.95, 2)), True, (9, 197, 9))
            self.surface.blit(fire_rate_text, (184, 684))

            self.surface.blit(self.range_icon, (164, 705))
            range_text = self.stats_font.render(str(int(round(tower.range*1.1, 0))), True, (9, 197, 9))
            self.surface.blit(range_text, (184, 707))

        #Disabled transparent rectangle if button is disabled
        if tower == None or tower.level == 10 or money < tower.upgrade_cost:
            self.surface.blit(self.disabled_rect, (self.bounds[0][0], self.bounds[1][0]))
        
        #Or hovered transparent rectangle if hovered over and not tower or disabled
        elif self.within_bounds(mouse_pos):
            self.surface.blit(self.hover_rect, (self.bounds[0][0], self.bounds[1][0]))