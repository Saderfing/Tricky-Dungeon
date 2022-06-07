import pygame
from boss import Livid
from utilities import Vec2
from random import randint
from generation import Generator
from bestiary import Goblin
from utilities import Vec2

class GameManager:
    def __init__(self, generator:Generator) -> None:
        self.gen = generator
        self.room_mob_dict = dict()

        self.isBossSpawned = False
        self.livid = None
        
        self.loaded_mob = dict()
        self.targets = self.loaded_mob.values() + self.livid if self.livid is not None else self.loaded_mob.values()
        
        self.SIM_DIST = 400
        self.TSIZE = 50

        self.chest = None
        self.potions = []

    def spawn_mob(self, map_rect):
        room_index = 0
        mob_dict = dict()
        for room in self.gen.room_list:
            for mob in range(room.num_mob):
                mob_dict[str(room_index) + str(mob)]  = Goblin([randint(room.topleft[0] * self.TSIZE, room.downright[0]* self.TSIZE - 22), randint(room.topleft[1]*self.TSIZE, room.downright[1] * self.TSIZE) - 22], 100, randint(0, 4), 2, 10, map_rect)
            room_index += 1
        self.room_mob_dict = mob_dict

    def spawn_livid(self, rects):
        self.livid = Livid([self.gen.room_list[-1].center[0] * self.TSIZE, self.gen.room_list[-1].center[1] * self.TSIZE], rects, 3, 100)
        self.loaded_mob["livid"] = self.livid
        self.isBossSpawned = True

    def update(self, player):
        self.targets = [i for i in self.loaded_mob.values()] + [self.livid] if self.livid is not None else self.loaded_mob.values()
        
        if self.isBossSpawned:
            print("e")
            livid_state = self.livid.update(player)
            print(livid_state)
            if livid_state <= 0:
                self.livid = None
                if 'livid' in self.loaded_mob.keys():
                    self.loaded_mob['livid'] = None
                self.isBossSpawned = False
            
        ispot = self.chest.update(player)
        if not ispot == 0:
            self.potions.append(ispot)
        for pot in range(len(self.potions)):
            self.potions[pot].update(player)
            if self.potions[pot].used:
                self.potions.pop(pot)

    def create_chest(self):
        for room in self.gen.room_list:
            if room.room_type == "chest":
                self.chest = Chest(room.center)

    def load_mob(self, player_pos):
        self.loaded_mob = dict()
        player_pos_v = Vec2(player_pos[0], player_pos[1])

        for mob in self.room_mob_dict.keys():

            the_mob = self.room_mob_dict[mob]
            mob_room = mob[0]
            mob_pos_v = Vec2(the_mob.pos[0], the_mob.pos[1])

            if Vec2.Distance(player_pos_v, mob_pos_v) < self.SIM_DIST:
                self.loaded_mob[mob] = self.room_mob_dict[mob]

    def check_mob_life(self):
        loaded =  self.loaded_mob.copy()
        room_mob = self.room_mob_dict.copy()
        isChanged = False
        for mob in self.loaded_mob.keys():
            if self.loaded_mob[mob].health <= 0:
                isChanged = True
                loaded.pop(mob)
                room_mob.pop(mob)
        if isChanged:
            self.loaded_mob = loaded.copy()
            self.room_mob_dict = room_mob.copy()

    def create_mob(self):
        self.gen.generate()


class Chest:
    def __init__(self, pos) -> None:
        self.pos = [pos[0] * 50, pos[1]*50]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 52, 50)
        self.content = ["potion"]
        self.opened = False

    def update(self, player):
        potion = 0
        if Vec2.Distance(Vec2(self.pos[0], self.pos[1]), Vec2(player.pos[0], player.pos[1])) < 100:
            if not self.opened:
                self.opened = True
                potion = Potion([self.pos[0]- 50, self.pos[1] + 50])
        return potion

class Potion:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 50)
        self.GFX = pygame.transform.scale(pygame.image.load("assets/potion.png"), (40, 40)) .convert_alpha()
        self.used = False

    def update(self, player):
        health_amount = 30
        if self.rect.colliderect(player.rect):
            player.health += health_amount
            if player.health > player.BASE_HP: player.health = player.BASE_HP
            self.used = True
