from entity import Entity
import pygame, sys
from utilities import Vec2
from random import randint

class Goblin(Entity):
    def __init__(self, pos: list, HP: int, DF: int, SP: int, DMG: int, map_rect:list):
        self.GFX = pygame.Surface((20,20))
        self.GFX.fill((125,0,0))
        self.sight_distance = 400
        self.map_rect = map_rect

        super().__init__(pos, self.GFX, HP, DF, SP, DMG)

        self.speed = self.speed * (randint(75,150) / 100)

        self.current_time = 0
        self.collide_time = 0
    
    def update(self, player):
        check_collide = self.pathfind(player.pos)
        if check_collide:
            self.collide()
        self.current_time = pygame.time.get_ticks()
        self.attack(player)

        self.apply_movement()

    def pathfind(self, pos:list):
        check_collide = True
        local_pos = Vec2(pos[0] - self.pos[0], pos[1] - self.pos[1])
        direction = local_pos.normalized()

        if Vec2.Distance(Vec2(pos[0], pos[1]), Vec2(self.pos[0], self.pos[1])) < self.sight_distance:
            self.velocity = [direction.x * self.speed, direction.y * self.speed]
        else:
            self.velocity = [0,0]
            check_collide = False
        return check_collide
        
    def collide(self):
        TSIZE = 50
        for rect_row in range(max(0, int(self.pos[1]/TSIZE) - self.SIMULATION_DISTANCE), min(len(self.map_rect), int(self.pos[1]/TSIZE) + self.SIMULATION_DISTANCE)):
            for rect_line in range(max(0, int(self.pos[0]/TSIZE) - self.SIMULATION_DISTANCE), min(len(self.map_rect[rect_row]), int(self.pos[0]/TSIZE) + self.SIMULATION_DISTANCE)):
                rect = self.map_rect[rect_row][rect_line]
                if rect is None:
                    pass
                else:
                    if rect.colliderect(self.pos[0] + self.velocity[0], self.pos[1], self.width, self.height):
                        self.velocity[0] = 0
                    if rect.colliderect(self.pos[0], self.pos[1]  + self.velocity[1], self.width, self.height):
                        self.velocity[1] = 0

    def apply_movement(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.center = [self.pos[0] + int(self.width/2), self.pos[1] + int(self.height/2)]

    def attack(self, player):
        if self.rect.colliderect(player.rect) and self.current_time - self.collide_time > 500:
            self.collide_time = pygame.time.get_ticks()
            player.apply_damage(self.dmg)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((854, 480))
    goblintest = Goblin([0,0],100, 1, 1, 10)

    test_collision = pygame.Surface((100,50)).convert()
    test_collision_rect = test_collision.get_rect(topleft = (200,200))
    clock = pygame.time.Clock()
    run = True
    while run:
        screen.fill((40,40,40))
        goblintest.update([[test_collision_rect]])
        screen.blit(test_collision, test_collision_rect)
        screen.blit(goblintest.GFX, goblintest.pos)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)
