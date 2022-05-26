import pygame
import render
import generation

pygame.init()

screen_size = (1280,720) #
screen = pygame.display.set_mode(screen_size)
renderer = render.Render(screen)


gen = generation.Generator([60,40])
gen.generate()

clock = pygame.time.Clock()

while renderer.run:

    renderer.draw_tilemap(gen.the_map)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            renderer.run = False
            pygame.quit()
    
    clock.tick(renderer.FPS)
    

