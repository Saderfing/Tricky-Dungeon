from entity import Entity, Player
import pygame
from random import randint

class Livid(Entity):
    def __init__(self, pos:list) -> None:
        GFX = pygame.image.load('assets/livid.png').convert_alpha()
        HP, DF, SP, DMG = 1000, 50, 10, 100
        
        super().__init__(pos, GFX, HP, DF, SP, DMG)
        
        self.phases = {0:self.shadow_dupes}
        self.current_phase = 0
        self.shadows = []
        
    def update(self):
        pass
    
    def pathfinding(self):
        pass
    
    def shadow_daggers(self):
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()