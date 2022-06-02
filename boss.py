from entity import Entity, Player, Projectil
import pygame
from random import randint
import math

class Livid(Entity):
    def __init__(self, pos:list) -> None:
        GFX = pygame.image.load('assets/livid.png').convert_alpha()
        HP, DF, SP, DMG = 1000, 50, 10, 100
        
        super().__init__(pos, GFX, HP, DF, SP, DMG)
        
        self.phases = {0:self.shadow_dupes}
        self.current_phase = 0
        self.shadows = []
        self.daggers = []
        self.daggers_angle = math.pi/6
        
    def update(self):
        self.shadow_daggers()
        self._child_manager()
    
    def pathfinding(self):
        pass
    
    def shadow_daggers(self):
        for i in range(6):
            self.daggers.append(Projectil(self.pos.copy(), i*self.daggers_angle, 10, 10, 'assets/shadow_daggers.png'))
    
    def _child_manager(self):
        for dagger in self.daggers:
            dagger.update()
            
        for shadow in self.shadows:
            shadow.update()
    
    def dash(self):
        pass
    
    def shadow_dupes(self):
        for i in range(4):
            self.shadows.append(Shadows((self.pos[0] + randint(-10, 10), self.pos[1] + randint(-10, 10))))
    
class Shadows(Livid):
    def __init__(self, pos: list) -> None:
        super().__init__(pos)


    
if __name__ == '__main__':
    #pygame.init()

    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player([0, 0], 100, 50, 10, 10, [])
    boss = Livid([WIDTH//2,HEIGHT//2])

    clock = pygame.time.Clock()
    FPS = 60
    while True:
        clock.tick(FPS)

        win.fill((0,0,0))
        player.update([WIDTH, HEIGHT])
        boss.update()
        win.blit(player.GFX, player.pos)
        win.blit(boss.GFX, boss.pos)
        for arrow in player.shot_arrows:
            win.blit(arrow.GFX, arrow.pos)
        for shadow in boss.shadows:
            win.blit(shadow.GFX, shadow.pos)
        for projectil in boss.daggers:
            win.blit(projectil.GFX, projectil.pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()