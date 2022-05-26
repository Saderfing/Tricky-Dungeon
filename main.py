import pygame
import render
import generation

pygame.init()

screen_size = (854, 480)
screen = pygame.Surface(screen_size)
window_size = (854, 480)
window = pygame.display.set_mode(window_size)
renderer = render.Render(screen, window)


gen = generation.Generator([40,20])
gen.generate()

clock = pygame.time.Clock()

while renderer.run:
    
    renderer.draw_tilemap(gen.the_map)
    renderer.display.blit(renderer.screen,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            renderer.run = False
            pygame.quit()

