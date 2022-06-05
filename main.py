from random import randint
import pygame, sys
from boss import Livid
import render
import generation
from entity import Player
from bestiary import Goblin
from game import GameManager

pygame.init()

HEIGHT = 720
WIDTH = 1280

screen_size = (WIDTH, HEIGHT) #
screen = pygame.display.set_mode(screen_size)   
renderer = render.Render(screen)

gen = generation.Generator([120, 120])
gen.generate()

gameManager = GameManager(gen)
gameManager.spawn_mob(renderer.get_rect_list(gen.the_map))

player = Player([gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ], 100, 5, 5, 50,  renderer.get_rect_list(gen.the_map))

clock = pygame.time.Clock()

while renderer.run:
    player.update([WIDTH, HEIGHT], gameManager.loaded_mob.values())
    gameManager.load_mob(player.pos)
    
    for mob in gameManager.loaded_mob.values():
        mob.update(player)
        
    renderer.calculate_scroll(player)

    renderer.screen.fill((33, 38, 63))
    renderer.draw_tilemap(gen.the_map, player)
    renderer.draw_debug(clock)
    renderer.draw_player(player)
    
    for arrow in player.shot_arrows:
        renderer.draw_object(arrow)
        pygame.draw.rect(screen, [255, 0, 0], pygame.Rect(arrow.rect.x - renderer.player_scroll[0], arrow.rect.y - renderer.player_scroll[1], arrow.width, arrow.height))
    
    for mob in gameManager.room_mob_dict.values():
        renderer.draw_object(mob)
        pygame.draw.rect(screen, [255, 0, 0], pygame.Rect(mob.rect.x - renderer.player_scroll[0], mob.rect.y - renderer.player_scroll[1], mob.width, mob.height))
    

    gameManager.check_mob_life()
    pygame.draw.rect(screen, [0, 0, 255], player.rect)
    renderer.draw_hud(player, gameManager.loaded_mob)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            renderer.run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gen.generate()
                player.pos = [gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ]
                player.the_map = renderer.get_rect_list(gen.the_map)

    clock.tick(renderer.FPS)
