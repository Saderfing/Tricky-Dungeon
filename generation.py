import random as rand
class Room:
    def __init__(self,size_x:int, size_y:int, num_mob:int, room_type:str) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.num_mob = num_mob
        self.position = []
        self.room_type = room_type
    def set_position(self,new_pos:list):
        self.position = new_pos

class RoomManager:
    @classmethod
    def __init__(self, num_room:int) -> None:
        self.num_room = num_room
        self.small_room = Room(3,3,0, "small")
        self.medium_room = Room(5,5,0, "medium")
        self.big_room = Room(7,7,0,"big")
        self.normal_room = [self.small_room,self.medium_room,self.big_room]

class Generator:
    def __init__(self, map_size:list) -> None:
        self.num_room = 1
        self.map_size = map_size
        self.the_map = []
        self.room_list = []

        self.roomManager = RoomManager(6)
    
    def create_empty_map(self):
        self.the_map = [[1 for x in range(self.map_size[0])] for y in range(self.map_size[1])]
    
    def place_room(self):
        for i in range(self.roomManager.num_room):
            room_to_place = rand.choice(self.roomManager.normal_room)
            try_place_x = rand.randint(1,self.map_size[0]-1-room_to_place.size_x)
            try_place_y = rand.randint(1,self.map_size[1]-1-room_to_place.size_y)
            print("pos x", try_place_x, "pos y", try_place_y)

            for room in self.room_list:
                print(room)
                while try_place_x >= room.position[0] and try_place_x  <= room.position[0]+ room.size_x and try_place_x + room_to_place.size_x >= room.position[0] and try_place_x + room_to_place.size_x <= room.position[0]:
                    
                    try_place_x = rand.randint(1,self.map_size[0]-1-room_to_place.size_x)
                    try_place_y = rand.randint(1,self.map_size[1]-1-room_to_place.size_y)
                    print("place found")
                

            
            self.room_list.append(Room(room_to_place.size_x,room_to_place.size_y,room_to_place.num_mob, room_to_place.room_type))
            print(self.room_list)
            
            for y in range(try_place_y, try_place_y+room_to_place.size_y):
                for x in range(try_place_x, try_place_x +room_to_place.size_x):
                    self.the_map[y][x] = 0

if __name__ == "__main__":
    generator = Generator([40,20])
    generator.create_empty_map()
    generator.place_room()
    
    print(generator.the_map)