import pygame
from random import randint
import math
from utilities import Vec2

class Entity:
    def __init__(self, pos:list, GFX, HP:int, DF:int, SP:int, DMG:int):
        self.pos = pos
        self.GFX = GFX
        self.width = self.GFX.get_width()
        self.height = self.GFX.get_height()
        
        self.center = [self.pos[0] + int(self.width/2), self.pos[1] + int(self.height/2)]
        
        rect = self.GFX.get_rect()
        self.rect = pygame.Rect(rect.x + self.pos[0], rect.y + self.pos[1], self.width*2, self.width*2)

        self.SIMULATION_DISTANCE = 3

        self.BASE_HP = HP
        self.BASE_DF = DF
        self.BASE_SP = SP
        self.BASE_DMG = DMG

        self.health = HP
        self.defence = DF
        self.speed = SP
        self.dmg = DMG

        self.velocity = [0, 0] # 2 integers to represent the x and y velocity

    def apply_damage(self, damage):
        
        health = self.health
        health -= damage
        if health <= 0:
            health = 0
        self.health = health

class Projectil:
    def __init__(self, pos:list, angle:int, damage:int, speed:int, graphics_path:str, life_time:int) -> None:
        self.pos = pos
        self.angle = angle
        self.life_time = life_time

        self.speed = speed
        self.DMG = damage
        self.velocity = [math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed]

        self.GFX = pygame.image.load(graphics_path).convert_alpha()
        self.GFX = pygame.transform.rotate(self.GFX, -math.degrees(self.angle))
        self.width = self.GFX.get_width()
        self.height = self.GFX.get_height()
        
        self.rect = self.GFX.get_rect(topleft=self.pos)
        
    def update(self, targets:list):
        self.attack(targets)
        if self.life_time <= 0:
            return -1

        self.life_time -= 1
        
        self.apply_movement()
        
    def apply_movement(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def attack(self, targets:list):
        for target in targets:
            if self.rect.colliderect(target.rect):
                target.apply_damage(self.DMG)
                self.life_time = 0
                            
class Player(Entity):
    def __init__(self, pos: list, HP: int, DF: int, SP: int, DMG: int, the_map):
        graphics = pygame.transform.scale(pygame.image.load('assets/player.png'), (22,22)).convert_alpha()
        super().__init__(pos, graphics, HP, DF, SP, DMG)
        self.angle = 0
        self.GFX.set_colorkey((0,0,0))

        self.the_map = the_map
        self.dungeon_niv = 0
        
        self.arrows = 5
        self.arrow_speed = 10
        self.shot_arrows = []
        self.cooldown = 350
        self.on_cooldown = False
        self.last_shot = pygame.time.get_ticks()
        self.refill_arrows = 2000 # time between new arrow
        self.REFILL_TIME = 2000

        self.keys = {pygame.K_UP: 0,
                     pygame.K_DOWN: 0,
                     pygame.K_RIGHT: 0,
                     pygame.K_LEFT: 0,
                     pygame.K_SPACE: 0}
        self.mouse = [0, 0, 0]
        self.PLAYER_DIE = pygame.USEREVENT + 1

    def update(self, screen_size, mobs):
        if self.health <= 0:
            pygame.event.post(pygame.event.Event(self.PLAYER_DIE))
        self._check_inputs()
        self._get_mouse_angle(screen_size)

        self.reload_arrow()
        self.shoot()
        if len(self.shot_arrows) > 0:
            self.arrow_manager(mobs)

        self.input_movement()

        self._check_collision()

        self.apply_movement()

    def _get_mouse_angle(self, screen_size):
        point = pygame.mouse.get_pos()
        mid = [screen_size[0]//2, screen_size[1]//2]

        vect = Vec2(point[0] - mid[0], point[1] - mid[1])
        vect = vect.normalized()
        angle = math.atan2(vect.y, vect.x)
        
        self.angle = angle

    def reload_arrow(self):
        if pygame.time.get_ticks() -  self.refill_arrows >= 0:
            self.arrows += 1
            self.refill_arrows = pygame.time.get_ticks() + self.REFILL_TIME
            
    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            self.on_cooldown = False

        if self.mouse[0] and self.arrows > 0 and not self.on_cooldown:
            self.shot_arrows.append(Projectil(self.pos.copy(), self.angle, self.dmg, self.arrow_speed, 'assets/arrow.png', 100))
            self.on_cooldown = True
            self.last_shot = pygame.time.get_ticks()
            self.arrows -= 1


    def arrow_manager(self, mobs):
        for arrow, index in zip(self.shot_arrows, range(len(self.shot_arrows))):
            state = arrow.update(mobs)
            if state == -1:
                self.shot_arrows.pop(index)

    def input_movement(self):
        self.velocity[0] = (self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed
        self.velocity[1] = (self.keys[pygame.K_DOWN] - self.keys[pygame.K_UP]) * self.speed

    def _check_collision(self):
        TSIZE = 50
        for rect_row in range(max(0, int(self.pos[1]/TSIZE) - self.SIMULATION_DISTANCE), min(len(self.the_map), int(self.pos[1]/TSIZE) + self.SIMULATION_DISTANCE)):
            for rect_line in range(max(0, int(self.pos[0]/TSIZE) - self.SIMULATION_DISTANCE), min(len(self.the_map[rect_row]), int(self.pos[0]/TSIZE) + self.SIMULATION_DISTANCE)):
                rect = self.the_map[rect_row][rect_line]
                if rect is None:
                    pass
                else:
                    if rect.colliderect(self.pos[0] + self.velocity[0], self.pos[1], self.width, self.height):
                        self.velocity[0] = 0
                    if rect.colliderect(self.pos[0], self.pos[1]  + self.velocity[1], self.width, self.height):
                        self.velocity[1] = 0

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
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
