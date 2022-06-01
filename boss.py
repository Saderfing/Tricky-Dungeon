from entity import Entity, Player
import pygame

class Schwamm(Entity):
    def __init__(self, pos:list) -> None:
        GFX = pygame.image.load('assets/Schwamm.png').convert_alpha()
        HP, DF, SP, DMG = 1000, 50, 10, 100
        
        super().__init__(pos, GFX, HP, DF, SP, DMG)
        
        self.phases = {}
        
    def update(self):
        pass
    
    def pathfinding(self):
        pass
    
    def water_splash(self):
        pass
    
    
if __name__ == '__main__':
    #pygame.init()

    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player([0, 0], 100, 50, 10, 10, [])
    boss = Schwamm([0,0])

    clock = pygame.time.Clock()
    FPS = 60
    while True:
        clock.tick(FPS)

        win.fill((0,0,0))
        player.update([WIDTH, HEIGHT], [0, 0])
        win.blit(player.GFX, player.pos)
        win.blit(boss.GFX, boss.pos)
        for arrow in player.shot_arrows:
            win.blit(arrow.GFX, arrow.pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()