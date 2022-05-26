import pygame

class Render:
    def __init__(self, screen:pygame.Surface, display:pygame.Surface ) -> None:
        self.screen = screen
        self.display = display
        
        self.TILE_SIZE = 16
        self.FPS = 60

        self.run = True

        self.textures = {0:pygame.Surface((self.TILE_SIZE,self.TILE_SIZE)), 1:pygame.Surface((self.TILE_SIZE,self.TILE_SIZE))}
        for i in self.textures.keys():
            if i == 1: self.textures[i].fill((20,20,20)) 
            if i == 0: self.textures[i].fill((255,255,255))
    
    def draw_tilemap(self, tiles:list):
        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
                self.screen.blit(self.textures[tiles[y][x]],(x*self.TILE_SIZE,y*self.TILE_SIZE))
    
    def draw_player(self,player):
        pass
    def draw_debug(self):
        pass
    def get_rect_list(self,the_map:list):
        rect_list = []

        for y in range(len(the_map)):
            for x in range(len(the_map[y])):
                if the_map[y][x] == 0:
                    rect_list.append(pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)).get_rect(topleft=(x*self.TILE_SIZE, y*self.TILE_SIZE)))
        return rect_list