import pygame
from random import randint

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


    

class Player(Entity):
    def __init__(self, pos: list, HP: int, DF: int, SP: int, DMG: int):
        HP, DF, SP, DMG = 100, 50, 1, 10
        graphics = pygame.image.load('assets/player.png').convert_alpha()
        super().__init__(pos, graphics, HP, DF, SP, DMG)
        self.arrows = 5
        self.fire_rate = 1
        self.cooldown = 1
        
        self.keys = {pygame.K_UP: 0, 
                     pygame.K_DOWN: 0, 
                     pygame.K_RIGHT: 0, 
                     pygame.K_LEFT: 0, 
                     pygame.K_SPACE:0}

        
    def update(self):
        self.input_movement()
        self.apply_movement()

    def input_movement(self):
            
        self._check_inputs()
        
        self.velocity[0] = (self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed
        self.velocity[1] = (self.keys[pygame.K_DOWN] - self.keys[pygame.K_UP]) * self.speed
        
    def _check_inputs(self):
        inputs = pygame.key.get_pressed()
        for key in self.keys.keys():
            self.keys[key] = inputs[key]
    
    def apply_movement(self):
        if self.pos[0] + self.velocity[0] < 0 or self.pos[0] + self.velocity[0] + self.width >= 800:
            self.velocity[0] = 0

        if self.pos[1] + self.velocity[1] < 0 or self.pos[1] + self.velocity[1] + self.height >= 400:
            self.velocity[1] = 0

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
        
