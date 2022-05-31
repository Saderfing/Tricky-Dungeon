import pygame

class Render:
    def __init__(self, screen:pygame.Surface) -> None:
        self.screen = screen

        self.TILE_SIZE = 50
        self.FPS = 60
        self.RENDER_DISTANCE = 15
        self.toggled_fps = True
        self.player_scroll = [0,0]

        self.run = True

        self.textures = {1:self._scale(pygame.image.load("assets/tiles/wall3.png")).convert(),

                         2:self._scale(pygame.image.load("assets/tiles/wall5.png")).convert(),
                         3:self._scale(pygame.image.load("assets/tiles/wall6.png")).convert(),
                         10:self._scale(pygame.image.load("assets/tiles/floor3.png")).convert(),
                         11:self._scale(pygame.image.load("assets/tiles/floor4.png")).convert(),
                         12:self._scale(pygame.image.load("assets/tiles/floor5.png")).convert(),
                         13:self._scale(pygame.image.load("assets/tiles/floor2.png")).convert()}


    def draw_tilemap(self, tiles:list):
        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
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
                if the_map[y][x] < 10:
                    rect_list.append(pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)).get_rect(topleft=(x*self.TILE_SIZE, y*self.TILE_SIZE)))
        return rect_list


    def _scale(self, image:pygame.Surface):
        return pygame.transform.scale(image,  (self.TILE_SIZE, self.TILE_SIZE))

