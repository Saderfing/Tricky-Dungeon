from entity import *
import pygame
from random import randint, choices
import math
from utilities import Vec2

class Livid(Entity):
    def __init__(self, pos:list, map_rect:list, speed=7) -> None:
        GFX = pygame.image.load('assets/livid.png').convert_alpha()
        HP, DF, SP, DMG = 1000, 50, speed, 10
        
        super().__init__(pos, GFX, HP, DF, SP, DMG)
        self.sight_distance = 1000
        self.map_rect = map_rect
        
        self.last_hit = 0
        self.attack_speed = 500
        self.SUPER_SPEED = 15
        self.jump_start = 0
        self.jump_time = 5000
        self.jump_cooldown = 5000
        self.next_jump = 0
        
        self.phases = [self._shadow_dupes, self._shadow_daggers, self._shadow_jump, self._shadow_snipe] # all the phases call
        self.phases_wheight = [0 for i in range(len(self.phases))]
        self.phase_indexs = [i for i in range(len(self.phases))]
        self.current_phase = 0 # index of the function of the corresponding phase
        self.new_phase = 100 # time between phases
        self.new_phase_delta = 0
        
        self.shadows = []   # store shadows:Shadows child
        self.daggers = []   # store daggers:Projectiles child
        self.daggers_angle = math.pi/6 
        self.delta_angle = 0 # random angle added for randomness to "Shadow daggers attack"
        
        self.player = None
        
    def update(self, player):
        self.player = player
        self.attack()
        check_collide = self.pathfind(self.player.pos)
        if check_collide:
            self.collide()
            
        self.apply_movement()
        self.phases[self.current_phase]()
        self._child_manager()

    def pathfind(self, pos:list):
        check_collide = True
        local_pos = Vec2(pos[0] - self.pos[0], pos[1] - self.pos[1])
        direction = local_pos.normalized()

        if Vec2.Distance(Vec2(pos[0], pos[1]), Vec2(self.pos[0], self.pos[1])) < self.sight_distance:
            self.velocity = [direction.x * self.speed, direction.y * self.speed]
        else:
            self.velocity = [0, 0]
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

    def _check_player_distance(self):
        player_vect = Vec2(self.player.pos[0], self.player.pos[1])
        self_vect = Vec2(self.pos[0], self.pos[1])
        dist = Vec2.Distance(player_vect, self_vect)
        return round(dist)
    
    def attack(self):
        dist = self._check_player_distance()
        if dist <= 50 and pygame.time.get_ticks() - self.last_hit >=0:
            self.player.apply_damage(self.dmg)
            self.last_hit = pygame.time.get_ticks() + self.attack_speed 
        
        if pygame.time.get_ticks() - self.new_phase - self.new_phase_delta >= 0:
            self.phases_wheight[0] += 5
            self.phases_wheight[1] += 5
            self.phases_wheight[2] += 9 if dist >= 500 and pygame.time.get_ticks() - self.next_jump else 0
            self.phases_wheight[3] += 7 if dist >= 500 else 5

            total = 0
            
            for i in self.phases_wheight:
                total += i
            
            self.phases_wheight = list(map(lambda x:x/total, self.phases_wheight))
            print(self.phase_indexs, self.phases_wheight)
            self.current_phase = choices(self.phase_indexs, self.phases_wheight)[0]
            print(self.current_phase)
            
            
    def _child_manager(self):
        for dagger, index in zip(self.daggers, range(len(self.daggers))):
            state_dagger = dagger.update([self.player])
            if state_dagger == -1:
                self.daggers.pop(index)
        
        for shadow, index in zip(self.shadows, range(len(self.shadows))):
            state_shadow = shadow.update()
            if state_shadow == -1:
                self.shadows.pop(index)
       
    def _shadow_daggers(self):
        for i in range(12):
            self.daggers.append(Projectil(self.pos.copy(), i*self.daggers_angle, 10, 10, 'assets/shadow_daggers.png', 50))

    def _shadow_jump(self):
        self.speed = 15

    def _shadow_dupes(self):
        if len(self.shadows) > 0:
            return 
        for i in range(4):
            self.shadows.append(Shadows([self.pos[0] + randint(-10, 10), self.pos[1] + randint(-10, 10)], self.map_rect))

    def _shadow_snipe(self):
        pass
    
class Shadows(Livid):
    def __init__(self, pos:list, map_rect:list) -> None:
        super().__init__(pos, map_rect, randint(5, 10))

    def update(self):
        pass
    
if __name__ == '__main__':
    #pygame.init()

    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player([0, 0], 100, 50, 10, 10, [])
    boss = Livid([WIDTH//2, HEIGHT//2], [])

    clock = pygame.time.Clock()
    FPS = 60
    while True:
        clock.tick(FPS)
        win.fill((0,0,0))
        player.update([WIDTH, HEIGHT], [boss, *boss.shadows])
        boss.update(player)
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