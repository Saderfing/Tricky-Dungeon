import random as rand
class Room:
    def __init__(self,size:list, topleft:list, num_mob:int, room_type:str) -> None:
        self.size_x = size[0]
        self.size_y = size[1]
        self.num_mob = num_mob
        self.topleft = topleft
        self.downright = [self.topleft[0] + self.size_x, self.topleft[1] + self.size_y]
        self.room_type = room_type
        self.center = [int((self.topleft[0] + self.downright[0])/2), int((self.topleft[1] + self.downright[1])/2)]

    def set_topleft(self,new_topleft:list):
        self.topleft = new_topleft
        self.downright = [self.topleft[0] + self.size_x, self.topleft[1] + self.size_y]
        self.center = [int((self.topleft[0] + self.downright[0])/2), int((self.topleft[1] + self.downright[1])/2)]

    def set_num_mob(self,new_num_mob:int):
        self.num_mob = new_num_mob


class RoomManager:
    def __init__(self, num_room:int) -> None:
        self.num_room = num_room
        self.small_room = [[10,10], "small"]
        self.medium_room =  [[14,14], "medium"]
        self.big_room = [[16,16], "big"]
        self.entrance_room = [[5,5], "entrance"]
        self.boss_room = [[17, 17], "boss"]
        self.chest_room = [[5,4], "chest"]
        self.normal_room = [self.small_room, self.medium_room, self.big_room]

        self.num_mob = {"small": 2, "medium": 4, "big": 5, "chest": 0, "boss": 6, "entrance": 0}

class Generator:
    def __init__(self, map_size:list) -> None:
        self.num_room = 1
        self.map_size = map_size
        self.the_map = []
        self.room_list = []

        self.roomManager = RoomManager(5)
        self.rect_list = []
    def _random_wall(self):
        random = rand.random() 
        if 0 < random < 0.01:
            return 2
        elif 0.01 < random < 0.02:
            return 3
        return 1
    def _random_floor(self):
        random = rand.random()
        if 0 < random < 0.01:
            return 11
        elif 0.01 < random < 0.02:
            return 12
        elif 0.03 < random < 0.05:
            return 13
        return 10
    def create_empty_map(self):
        self.the_map = [[self._random_wall() for x in range(self.map_size[0])] for y in range(self.map_size[1])]
    
    def place_room(self, room_type_list:list):
        
        room_to_place = rand.choice(room_type_list)
        try_place_x = rand.randint(1,self.map_size[0]-1-room_to_place[0][0])
        try_place_y = rand.randint(1,self.map_size[1]-1-room_to_place[0][1])

        new_room = Room(room_to_place[0], [try_place_x, try_place_y] ,self.roomManager.num_mob[room_to_place[1]], room_to_place[1])
        
        #print("pos x", try_place_x, "pos y", try_place_y)

        for room in self.room_list:
            
            while new_room.topleft[0] <= room.downright[0] and new_room.downright[0] >= room.topleft[0] and new_room.topleft[1] <= room.downright[1] and new_room.downright[1] >= room.topleft[1]:
                
                try_place_x = rand.randint(1,self.map_size[0]-room_to_place[0][0]-1)
                try_place_y = rand.randint(1,self.map_size[1]-room_to_place[0][1]-1)
                new_room.set_topleft([try_place_x, try_place_y])
                #print("---------- place not found ------------ ")
        #print("###################### Place found ######################")
        #print("pos x", try_place_x, "pos y", try_place_y)

        
        self.room_list.append(new_room)
        #print(self.room_list)
        
        for y in range(new_room.topleft[1], new_room.downright[1]):
            for x in range(new_room.topleft[0], new_room.downright[0]):
                self.the_map[y][x] = self._random_floor()
    
    def place_chest_room(self):
        
        room_to_place = self.roomManager.chest_room
        try_place_x = rand.randint(1,self.map_size[0]-1-room_to_place[0][0])
        try_place_y = rand.randint(1,self.map_size[1]-1-room_to_place[0][1])

        new_room = Room(room_to_place[0], [try_place_x, try_place_y] ,0, room_to_place[1])

        for room in self.room_list:
            
            while new_room.topleft[0] <= room.downright[0] and new_room.downright[0] >= room.topleft[0] and new_room.topleft[1] <= room.downright[1] and new_room.downright[1] >= room.topleft[1]:
                
                try_place_x = rand.randint(1,self.map_size[0]-room_to_place[0][0]-1)
                try_place_y = rand.randint(1,self.map_size[1]-room_to_place[0][1]-1)
                new_room.set_topleft([try_place_x, try_place_y])
                #print("---------- place not found ------------ ")
        #print("###################### Place found ######################")
        #print("pos x", try_place_x, "pos y", try_place_y)
        
        self.room_list.insert(rand.randint(0,len(self.room_list)), new_room)
        
        for y in range(new_room.topleft[1], new_room.downright[1]):
            for x in range(new_room.topleft[0], new_room.downright[0]):
                self.the_map[y][x] = self._random_floor()
    
    def place_entrance(self):
        random_pos_x = rand.randint(1,self.map_size[0]-1-self.roomManager.entrance_room[0][0])
        random_pos_y = rand.randint(1,self.map_size[1]-1-self.roomManager.entrance_room[0][1])
        new_entrance = Room(self.roomManager.entrance_room[0],[random_pos_x, random_pos_y], 0, self.roomManager.entrance_room[1])

        self.room_list.append(new_entrance)

        for y in range(new_entrance.topleft[1], new_entrance.downright[1]):
            for x in range(new_entrance.topleft[0], new_entrance.downright[0]):
                self.the_map[y][x] = self._random_floor()


    def make_corridor(self, pointA:list, pointB:list):
        width = 2 if rand.random() < .6 else 1
        if rand.random() > 0.5:
            corner_pos = [pointA[0], pointB[1]]
        else:
            corner_pos = [pointB[0], pointA[1]]
        

        for y in range(min(pointA[1], corner_pos[1]), max(pointA[1], corner_pos[1]+width)):
            for x in range(min(pointA[0], corner_pos[0]), max(pointA[0], corner_pos[0])+width):
                self.the_map[y][x] = self._random_floor()

        for y in range(min(pointB[1], corner_pos[1]), max(pointB[1], corner_pos[1]+width)):
            for x in range(min(pointB[0], corner_pos[0]), max(pointB[0], corner_pos[0])+width):
                self.the_map[y][x] = self._random_floor()
    
    def generate(self):
        self.__init__(self.map_size)
        self.create_empty_map()
        self.place_entrance()
        for i in range(self.roomManager.num_room):
            self.place_room(self.roomManager.normal_room)
        
        self.place_chest_room()

        self.place_room([self.roomManager.boss_room])
        
        for room in range(1, len(self.room_list)):
            self.make_corridor(self.room_list[room-1].center, self.room_list[room].center)



if __name__ == "__main__":
    import pygame
    import render_lib

    pygame.init()
    screen = pygame.display.set_mode((800,800))
    renderer = render_lib.Render(screen,(800,800))

    generator = Generator([120,120])
    generator.generate()
    

    while renderer.run:
        renderer.render_tile(generator.the_map)
        for event in pygame.event.get():
            # joueur quitte ?
            if event.type == pygame.QUIT:
                pygame.quit()
                renderer.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generator.generate()
    print(" ")
    #print(generator.the_map)