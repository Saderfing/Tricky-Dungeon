from entity import Entity
import pygame, sys
from utilities import Vec2

class Goblin(Entity):
    def __init__(self, pos: list, HP: int, DF: int, SP: int, DMG: int):
        self.GFX = pygame.Surface((16,16))
        self.GFX.fill((125,0,0))
        self.sight_distance = 200
        
        super().__init__(pos, self.GFX, HP, DF, SP, DMG)
    
    def update(self):
        self.pathfind(pygame.mouse.get_pos())
        #self.attack()
    
    def pathfind(self, pos:list):
        
        local_pos = Vec2(pos[0] - self.pos[0], pos[1] - self.pos[1])
        direction = local_pos.normalized()

        if Vec2.Distance(Vec2(pos[0], pos[1]), Vec2(self.pos[0], self.pos[1])) < self.sight_distance:
            self.velocity = [direction.x * self.speed, direction.y * self.speed]
        else:
            self.velocity = [0,0]
        self.apply_movement()
        
    def apply_movement(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
    
    def attack(self, player):
        if self.rect.colliderect(player.rect):
            print("toucher le joueur")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((854, 480))
    goblintest = Goblin([0,0],100, 1, 1, 10)
    clock = pygame.time.Clock()
    run = True
    while run:
        screen.fill((40,40,40))
        goblintest.update()
        screen.blit(goblintest.GFX, goblintest.pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)