import pygame
from random import randint

class Entity:
    def __init__(self, pos:list, HP:int, DF:int, SP:int, DMG:int):
        self.pos = pos
        
        self.BASE_HP = 0
        self.BASE_DF = 0
        self.BASE_SP = 0
        self.BASE_DMG = 0
        
        self.health = HP
        self.defence = DF
        self.speed = SP
        self.damage = DMG
        
class Player(Entity):
    def __init__(self, pos: tuple, HP: int, DF: int, SP: int, DMG: int):
        HP, DF, SP, DMG = 100, 50, 3, 10
        super().__init__(pos, HP, DF, SP, DMG)
        self.arrows = 5
        self.fire_rate = 1
        self.cooldown = 1
        
        self.controls_weight = {pygame.K_DOWN:1,
                         pygame.K_UP:-1,
                         pygame.K_LEFT:-1,
                         pygame.K_RIGHT:1,
                         pygame.K_z:-1,
                         pygame.K_s:1,
                         pygame.K_q:-1,
                         pygame.K_d:1}
        self.pomme = 0
        
        #self.velocity = [0, 0] # 2 integers to represent the x and y velocity
        
    def update(self):
        self.pos += self.movement()
        
    def movement(self):
        vector = [0, 0]
        
        print(pygame.K_UP)
        
if __name__ == '__main__':
    import pygame
    from sys import exit


    pygame.init()
    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        
        print(pygame.K_z)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        pygame.display.update()
        
