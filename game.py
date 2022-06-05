import pygame
from utilities import Vec2
from random import randint
from generation import Generator
from bestiary import Goblin

class GameManager:
    def __init__(self, generator:Generator) -> None:
        self.gen = generator
        self.room_mob_list = []

        self.loaded_mob = []
        
        self.SIM_DIST = 400
        self.TSIZE = 50
    
    def spawn_mob(self, map_rect):
        for room in self.gen.room_list:
            liste = []
            for mob in range(room.num_mob):
                liste.append(Goblin([randint(room.topleft[0] * self.TSIZE, room.downright[0]* self.TSIZE - 22), randint(room.topleft[1]*self.TSIZE, room.downright[1] * self.TSIZE) - 22], 20, randint(0, 4), 2, 5, map_rect))
            self.room_mob_list.append(liste)

    def load_mob(self, player_pos):
        self.loaded_mob = []
        player_pos_v = Vec2(player_pos[0], player_pos[1])
        
       
        for room in range(len(self.room_mob_list)):
            for mob in range(len(self.room_mob_list[room])):
                the_mob = self.room_mob_list[room][mob]
                mob_pos_v = Vec2(the_mob.pos[0], the_mob.pos[1])

                if Vec2.Distance(player_pos_v, mob_pos_v) < self.SIM_DIST:
                    self.loaded_mob.append(self.room_mob_list[room][mob])
    
    def create_mob(self):
        self.gen.generate()
