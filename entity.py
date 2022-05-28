import pygame
from random import randint
import math

class Entity:
    def __init__(self, pos:list, GFX,HP:int, DF:int, SP:int, DMG:int):
        self.pos = pos
        self.GFX = GFX
        self.rect = GFX.get_rect()
        self.width = self.GFX.get_width()
        self.height = self.GFX.get_height()
        
        self.BASE_HP = 0
        self.BASE_DF = 0
        self.BASE_SP = 0
        self.BASE_DMG = 0
        
        self.health = HP
        self.defence = DF
        self.speed = SP
        self.damage = DMG
        
        self.velocity = [0, 0] # 2 integers to represent the x and y velocity


class Arrow:
    def __init__(self, pos, angle, speed) -> None:
        self.pos = pos
        self.angle = angle
        self.speed = speed

        self.GFX = pygame.image.load('assets/arrow.png').convert_alpha()
    
    @classmethod
    def update(self):
        pass

class Player(Entity):
    def __init__(self, pos: list, HP: int, DF: int, SP: int, DMG: int):
        graphics = pygame.image.load('assets/player.png').convert_alpha()
        super().__init__(pos, graphics, HP, DF, SP, DMG)
        self.arrows = 5
        self.arrow_speed = 3
        self.shot_arrows = []
        self.fire_rate = 1
        self.cooldown = 1
        self.is_on_cooldown = False
        
        self.keys = {pygame.K_UP: 0, 
                     pygame.K_DOWN: 0, 
                     pygame.K_RIGHT: 0, 
                     pygame.K_LEFT: 0, 
                     pygame.K_SPACE:0}
        
        self.mouse = [0, 0, 0]
        
        

        
    def update(self):
        self._check_inputs()
        
        self.shoot()
        
        self.input_movement()
        self.apply_movement()
    
    def _get_mouse_angle(self):
        point = pygame.mouse.get_pos()
        
        dist_x = point[0] - self.pos[0] 
        dist_y = point[1] - self.pos[1]
        
        if dist_x == float(0): # avoid division by 0
            dist_x += 0.00001
        angle = math.atan2(dist_y, dist_x)

        angle = round(math.degrees(angle))
        return angle
        
    def shoot(self):
        if self.is_on_cooldown:
            return
        
        angle = self._get_mouse_angle()
        
        self.shot_arrows.append(Arrow(self.pos, angle, self.arrow_speed))

    def input_movement(self):
        
        self.velocity[0] = (self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed
        self.velocity[1] = (self.keys[pygame.K_DOWN] - self.keys[pygame.K_UP]) * self.speed
        
    def _check_inputs(self):
        key_inputs = pygame.key.get_pressed()
        mouse_inputs = pygame.mouse.get_pressed()
        for key in self.keys.keys():
            self.keys[key] = key_inputs[key]
        for mouse in range(len(self.mouse)):
            self.mouse[mouse] = int(mouse_inputs[mouse])
        
    
    def apply_movement(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    
if __name__ == '__main__':
    #pygame.init()
    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player([0, 0], 100, 50, 3, 10)
    
    while True:

        win.fill((0,0,0))
        win.blit(player.GFX, player.pos)

        player.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        pygame.display.update()
        
