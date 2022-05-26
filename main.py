import pygame, sys
import render
import generation

pygame.init()

screen_size = (1280,720) #
screen = pygame.display.set_mode(screen_size)
renderer = render.Render(screen)


gen = generation.Generator([100,100])
gen.generate()

clock = pygame.time.Clock()

while renderer.run:

    renderer.draw_tilemap(gen.the_map)
    renderer.draw_debug(clock)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            renderer.run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gen.generate()
    
    clock.tick(renderer.FPS)
    

