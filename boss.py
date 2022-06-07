from entity import *
import pygame
from random import randint, choices, random
import math
from utilities import Vec2

class Livid(Entity):
    def __init__(self, pos:list, map_rect:list, speed=5, HP=1000) -> None:
        GFX = pygame.image.load('assets/livid.png').convert_alpha()
        HP, DF, SP, DMG = 1000, 50, speed, 10
        
        super().__init__(pos, GFX, HP, DF, SP, DMG)
        self.sight_distance = 1000
        self.map_rect = map_rect
        self.current_time = pygame.time.get_ticks()
        
        self.last_hit = 0
        self.ATTACK_SPEED = 500
        self.PROJECTIL_SPEED = 10
        
        self.phases = [self._shadow_dupes, self._shadow_daggers, self._shadow_jump, self._shadow_snipe] # all the phases call
        self.phases_wheight = [0 for i in range(len(self.phases))]
        self.DISTANTE_ATTACK = [0.1, 0.1, 0.5, 0.3]
        self.NORMAL_ATTACK = [0.3, 0.3, 0.2, 0.2]
        self.PHASE_INDEXS = [i for i in range(4)]
        self.current_phase = 0 # index of the function of the corresponding phase
        self.new_phase = 1000 # time between phases
        
        self.new_phase_delta = 0
        
        self.shadows = []   # store shadows:Shadows child
        
        self.daggers = []   # store daggers:Projectiles child
        self.daggers_angle = math.pi/6 
        self.daggers_delta_angle = random() # random angle added for randomness to "Shadow daggers attack"
        self.daggers_last_shot = 0
        self.DAGGERS_COOLDOWN = 2000
           
        self.SUPER_SPEED = 10
        self.jump_start = 0
        self.isJumping = False
        self.JUMP_TIME = 5000
        self.JUMP_COOLDOWN = 5000
        self.next_jump = 0
        
        self.snipes = None   # store daggers:Projectiles child 
        self.snipe_last_shot = 0
        self.SNIPE_COOLDOWN = 5000
        
        self.player = None
        
    def update(self, player):
        self.current_time = pygame.time.get_ticks()
        self.player = player
        self.attack()
        
        if self.isJumping:
            self._check_jump()
        
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
        if dist <= 50 and self.current_time - self.last_hit >=0:
            self.player.apply_damage(self.dmg)
            self.last_hit = self.current_time + self.ATTACK_SPEED 
        
        if self.current_time - self.new_phase - self.new_phase_delta >= 0:
            self._choose_attack(dist)
            
    def _choose_attack(self, dist):
        self.phases_wheight = self.DISTANTE_ATTACK if dist >= 500 else self.NORMAL_ATTACK
        self.current_phase = choices(self.PHASE_INDEXS, self.phases_wheight)[0]
        self.new_phase = self.current_time
        self.new_phase_delta = randint(0, 1000)
            
    def _child_manager(self):
        for dagger, index in zip(self.daggers, range(len(self.daggers))):
            state_dagger = dagger.update([self.player])
            if state_dagger == -1:
                self.daggers.pop(index)
        
        for shadow, index in zip(self.shadows, range(len(self.shadows))):
            state_shadow = shadow.update(self.player)
            if state_shadow == -1:
                self.shadows.pop(index)
       
    def _shadow_daggers(self):
        if self.current_time - self.daggers_last_shot >= self.DAGGERS_COOLDOWN:
            for i in range(12):
                self.daggers.append(Projectil(self.pos.copy(), i*(self.daggers_angle+self.daggers_delta_angle), self.PROJECTIL_SPEED, 10, 'assets/shadow_daggers.png', 50))
            self.daggers_last_shot = self.current_time
 
    def _shadow_jump(self):
        if not self.isJumping and self.current_time - self.next_jump >= 0:
            self.speed = self.SUPER_SPEED
            self.next_jump = self.current_time + self.JUMP_COOLDOWN
            self.isJumping = True
            
        self._check_jump()
        
    def _check_jump(self):
        if self.current_time - self.JUMP_TIME >= 0:
            self.speed = self.BASE_SP

    def _shadow_dupes(self):
        if len(self.shadows) > 0:
            return 
        for i in range(4):
            self.shadows.append(Shadows([self.pos[0] + randint(-10, 10), self.pos[1] + randint(-10, 10)], self.map_rect))

    def _shadow_snipe(self):
        if self.current_time - self.snipe_last_shot >= 0:
            self.snipe_last_shot = self.current_time + self.SNIPE_COOLDOWN
            angle = self._aim_target()
            self.snipe_proj = Projectil(self.pos.copy(), angle, self.dmg, self.PROJECTIL_SPEED, "assets/shadow_daggers.png", 1000)
        
    def _aim_target(self):
        vect = Vec2(self.pos[0] - self.player.pos[0], self.pos[1] - self.player.pos[1])
        vect = vect.normalized()
        angle = math.atan2(vect.y, vect.x)
        
        return angle
    
class Shadows(Livid):
    def __init__(self, pos:list, map_rect:list) -> None:
        super().__init__(pos, map_rect, randint(5, 10), 1)

    def update(self, player):
        self.player = player
        self.current_time = pygame.time.get_ticks()
        self.attack()
        check_collide = self.pathfind(self.player.pos)
        if check_collide:
            self.collide()
            
        self.apply_movement()
        
    def attack(self):
        dist = self._check_player_distance()
        if dist <= 50 and self.current_time - self.last_hit >=0:
            self.player.apply_damage(self.dmg)
            self.last_hit = self.current_time + self.ATTACK_SPEED 
        
        if randint(0,3) == 0 and self.current_time - self.snipe_last_shot >= 0:
            self._shadow_snipe()

        
if __name__ == '__main__': 
    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player([0, 0], 100, 50, 10, 10, [])
    boss = Livid([WIDTH//2, HEIGHT//2], [])

    clock = pygame.time.Clock()
    FPS = 60
    while True:
        print(player.health)
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