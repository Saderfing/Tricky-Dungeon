import pygame

class Render:
    def __init__(self, screen:pygame.Surface) -> None:
        self.screen = screen

        self.TILE_SIZE = 50
        self.FPS = 60
        self.RENDER_DISTANCE = 16
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
        
        self.arrow_inv = pygame.transform.scale(pygame.image.load("assets/arrow_sideways.png"), (50, 50)).convert_alpha()
        
        self.defaultFont = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.m4f7 = pygame.font.Font("assets/m5x7.ttf", 40)

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

    def draw_object(self, obj):
        self.screen.blit(obj.GFX, (obj.pos[0] - self.player_scroll[0],  obj.pos[1]- self.player_scroll[1]))

    def draw_debug(self, clock:pygame.time.Clock):

        if self.toggled_fps: self.screen.blit(self.defaultFont.render(str(round(clock.get_fps())), True, (250,10,10)), (10,10))

    def get_rect_list(self,the_map:list):
        rect_list = [[None for x in range(len(the_map[y]))] for y in range(len(the_map))]

        for y in range(len(the_map)):
            for x in range(len(the_map[y])):
                if the_map[y][x] < 10:
                    rect_list[y][x] = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)).get_rect(topleft=(x*self.TILE_SIZE, y*self.TILE_SIZE))
        return rect_list


    def _scale(self, image:pygame.Surface):
        return pygame.transform.scale(image,  (self.TILE_SIZE, self.TILE_SIZE))
    
    def draw_hud(self, player, loaded_mob:list):
        self._draw_player_hp(player)
        self._draw_mob_hp(loaded_mob)
        self._draw_arrow_amount(player)
        #self._draw_ability()
    
    def _draw_arrow_amount(self, player):
        surf = self.m4f7.render(f"{player.arrows}", False, (255,255,255))
        self.screen.blit(self.arrow_inv, (self.screen.get_width() - self.arrow_inv.get_width() - 85, self.screen.get_height() - self.arrow_inv.get_height() -  30))
        self.screen.blit(surf, (self.screen.get_width() - surf.get_width() - 75, self.screen.get_height() - 55))
    
    def _draw_player_hp(self, player):
        hp_box = pygame.Surface((300, 40))
        hp_box.fill((169,59, 59))
        
        hp = pygame.Surface((int((player.health/player.BASE_HP)* 300), 40))
        hp.fill((182, 213, 60))

        hp_box.blit(hp, (0,0))
        self.screen.blit(hp_box, (self.screen.get_width()//2 - hp_box.get_width()//2, self.screen.get_height() - hp_box.get_height() - 30))
    
    def _draw_mob_hp(self, loaded_mob):
        pass