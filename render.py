import pygame
from utils import clamp

class Render:
    def __init__(self, screen:pygame.Surface) -> None:
        self.screen = screen

        self.TILE_SIZE = 50
        self.FPS = 60
        self.RENDER_DISTANCE = 20
        self.toggled_fps = True
        self.player_scroll = [0,0]

        self.run = True

        self.textures = {1:pygame.transform.scale(pygame.image.load("assets/tiles/wall3.png"), (self.TILE_SIZE, self.TILE_SIZE)).convert(),
                         0:pygame.transform.scale(pygame.image.load("assets/tiles/floor3.png"), (self.TILE_SIZE, self.TILE_SIZE)).convert()}
        """for i in self.textures.keys():
            if i == 1: self.textures[i].fill((20,20,20)) 
            if i == 0: self.textures[i].fill((255,255,255))"""
    
    def draw_tilemap(self, tiles:list, player):

        for y in range(max(int(player.pos[1]/self.TILE_SIZE) - self.RENDER_DISTANCE,  0), min(int(player.pos[1]/self.TILE_SIZE) + self.RENDER_DISTANCE, len(tiles))):
            for x in range(max(int(player.pos[0]/self.TILE_SIZE) - self.RENDER_DISTANCE,  0), min(int(player.pos[0]/self.TILE_SIZE) + self.RENDER_DISTANCE, len(tiles))):
                self.screen.blit(self.textures[tiles[y][x]],((x*self.TILE_SIZE)-self.player_scroll[0],(y*self.TILE_SIZE)-self.player_scroll[1]))
    def calculate_scroll(self, player):
        SCREEN_SIZE = self.screen.get_size()
        self.player_scroll[0] += int((player.pos[0] - self.player_scroll[0] - (SCREEN_SIZE[0]/2))/10)
        self.player_scroll[1] += int((player.pos[1] - self.player_scroll[1] - (SCREEN_SIZE[1]/2))/10)

    def draw_player(self,player):
        
        self.screen.blit(player.GFX, (player.pos[0] - self.player_scroll[0],  player.pos[1]- self.player_scroll[1]))
    def draw_debug(self, clock:pygame.time.Clock):
        defaultFont = pygame.font.Font(pygame.font.get_default_font(), 25)

        if self.toggled_fps: self.screen.blit(defaultFont.render(str(round(clock.get_fps())), True, (250,10,10)), (10,10))
    def get_rect_list(self,the_map:list):
        rect_list = []

        for y in range(len(the_map)):
            for x in range(len(the_map[y])):
                if the_map[y][x] == 0:
                    rect_list.append(pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)).get_rect(topleft=(x*self.TILE_SIZE, y*self.TILE_SIZE)))
        return rect_list