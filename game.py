import pygame
from utilities import Vec2
from random import randint
from generation import Generator
from bestiary import Goblin

class GameManager:
    def __init__(self, generator:Generator) -> None:
        self.gen = generator
        self.room_mob_dict = dict()

        self.loaded_mob = dict()
        
        self.SIM_DIST = 400
        self.TSIZE = 50
    
    def spawn_mob(self, map_rect):
        room_index = 0
        mob_dict = dict()
        for room in self.gen.room_list:
            for mob in range(room.num_mob):
                mob_dict[str(room_index) + str(mob)]  = Goblin([randint(room.topleft[0] * self.TSIZE, room.downright[0]* self.TSIZE - 22), randint(room.topleft[1]*self.TSIZE, room.downright[1] * self.TSIZE) - 22], 100, randint(0, 4), 2, 5, map_rect)
            room_index += 1
        self.room_mob_dict = mob_dict
            

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
