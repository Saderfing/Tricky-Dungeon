import uuid
import pygame
from random import randint
import math
from utilities import Vec2

class Entity:
    def __init__(self, pos:list, GFX, HP:int, DF:int, SP:int, DMG:int):
        self.uuid = uuid.uuid1()
        self.pos = pos
        self.GFX = GFX
        self.rect = GFX.get_rect()
        self.width = self.GFX.get_width()
        self.height = self.GFX.get_height()
        self.center = (self.width + self.height)//2

        self.BASE_HP = 0
        self.BASE_DF = 0
        self.BASE_SP = 0
        self.BASE_DMG = 0

        self.health = HP
        self.defence = DF
        self.speed = SP
        self.damage = DMG

        self.velocity = [0, 0] # 2 integers to represent the x and y velocity

    def damage(self, damage):
        damage = damage - self.defence
        self.health -= damage

class Projectil:
    def __init__(self, pos:list, angle:int, damage:int, speed:int, graphics_path:str, life_time:int) -> None:
        self.pos = pos
        self.angle = angle
        self.life_time = life_time
        
        self.speed = speed
        self.damage = damage
        self.velocity = [math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed]

        self.GFX = pygame.image.load(graphics_path).convert_alpha()

        self.rect = self.GFX.get_rect()
        self.width = self.GFX.get_width()
        self.height = self.GFX.get_height()
        self.center = (self.width + self.height)//2

    def update(self):
        if self.life_time <= 0:
            return -1
    
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.life_time -= 1
        return 0

class Player(Entity):
    def __init__(self, pos: list, HP: int, DF: int, SP: int, DMG: int, the_map):
        graphics = pygame.image.load('assets/player.png').convert_alpha()
        super().__init__(pos, graphics, HP, DF, SP, DMG)
        self.angle = self._get_mouse_angle([1280, 720])
        self.GFX.set_colorkey((0,0,0))
        
        self.the_map = the_map
        
        self.arrows = 5
        self.arrow_speed = 10
        self.shot_arrows = []
        self.cooldown = 1000
        self.on_cooldown = False
        self.last_shot = pygame.time.get_ticks()
        self.refill_arrows = 1000 # time between new arrow

        self.keys = {pygame.K_UP: 0,
                     pygame.K_DOWN: 0,
                     pygame.K_RIGHT: 0,
                     pygame.K_LEFT: 0,
                     pygame.K_SPACE: 0}
        self.mouse = [0, 0, 0]

    def update(self, screen_size):
        self._check_inputs()
        self._get_mouse_angle(screen_size)
        
        self.reload_arrow()
        self.shoot()

        self.input_movement()

        self._check_collision()
        
        self.apply_movement()

    def _get_mouse_angle(self, screen_size):
        point = pygame.mouse.get_pos()
        mid = [screen_size[0]//2, screen_size[1]//2]

        vect = Vec2(point[0] - mid[0], point[1] - mid[1])
        vect = vect.normalized()
        angle = math.atan2(vect.y, vect.x)
        
        #self.GFX = pygame.transform.rotate(self.GFX, self.angle)
        self.angle = angle

     def reload_arrow(self):
        if pygame.time.get_ticks() % self.refill_arrows == 0:

            self.arrows += 1


    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            self.on_cooldown = False

        if self.mouse[0] and self.arrows > 0 and not self.on_cooldown:
            self.shot_arrows.append(Projectil(self.pos.copy(), self.angle, self.damage, self.arrow_speed, 'assets/arrow.png', 100))
            self.on_cooldown = True
            self.last_shot = pygame.time.get_ticks()
            self.arrows -= 1

        if len(self.shot_arrows) > 0:
            self.arrow_manager()

    def arrow_manager(self):
        for arrow, index in zip(self.shot_arrows, range(len(self.shot_arrows))):
            state = arrow.update()
            if state == -1:
                self.shot_arrows.pop(index)
            print(self.shot_arrows)

    def input_movement(self):
        self.velocity[0] = (self.keys[pygame.K_RIGHT] - self.keys[pygame.K_LEFT]) * self.speed
        self.velocity[1] = (self.keys[pygame.K_DOWN] - self.keys[pygame.K_UP]) * self.speed

    def _check_collision(self):
        for rect in self.the_map:
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
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
if __name__ == '__main__':
    #pygame.init()

    WIDTH = 800
    HEIGHT = 400
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player([0, 0], 100, 50, 10, 10, [])

    clock = pygame.time.Clock()
    FPS = 60
    while True:
        clock.tick(FPS)

        win.fill((0,0,0))
        player.update([WIDTH, HEIGHT])
        win.blit(player.GFX, player.pos)
        for arrow in player.shot_arrows:
            win.blit(arrow.GFX, arrow.pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
