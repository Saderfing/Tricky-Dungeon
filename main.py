import pygame, sys
import render
import generation
from entity import Player

pygame.init()

screen_size = (1280,720) #
screen = pygame.display.set_mode(screen_size)
renderer = render.Render(screen)


gen = generation.Generator([120,120])
gen.generate()

player = Player([gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ], 100, 5, 4, 10)

clock = pygame.time.Clock()

while renderer.run:
    player.update()
    renderer.calculate_scroll(player)

    renderer.screen.fill((33, 38, 63))
    renderer.draw_tilemap(gen.the_map)
    renderer.draw_debug(clock)
    renderer.draw_player(player)

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
    
    clock.tick(renderer.FPS)
    

