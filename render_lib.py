import pygame
from random import randint


class Render:
    def __init__(self, screen:pygame.Surface, size:tuple) -> None:
        self.size = size

        self.clock = pygame.time.Clock()
        self.screen = screen

        self.WHITE = (255,255,255)
        self.FPS = 60
        self.TILE_SIZE = 5

        self.run = True
        self.toggled_fps = False
    def random_color(self):
        r = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        r.fill((randint(125,200), randint(125,200), randint(125,200)))
        return r
    def render_tile(self,tiles:list):
        
        surf_white = pygame.Surface((self.TILE_SIZE,self.TILE_SIZE))
        surf_white.fill(self.WHITE)
        self.screen.fill((0,0,0))

        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
                if tiles[y][x] != 1  : self.screen.blit(surf_white,(x*self.TILE_SIZE,y*self.TILE_SIZE))
        
        
        defaultFont = pygame.font.Font(pygame.font.get_default_font(), 25)

        if self.toggled_fps: self.screen.blit(defaultFont.render(str(self.clock.get_fps()), True, (250,10,10)), (10,10))
        pygame.display.update()
        self.clock.tick(self.FPS)
