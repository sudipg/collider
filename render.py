import pygame
import time
import sys
import numpy as np
from gridworld import *

pygame.init()
world = grid_world(15,15,20) 

screen = pygame.display.set_mode((world.height * world.cell_size, world.height * world.cell_size))

frame_count = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();
    world.update()
    time.sleep(1.0/60)
    screen.fill(EMPTY)
    for i in range(world.height):
        for j in range(world.width):
            pygame.draw.rect(screen, COLORS[world.cells[i][j].item], (j*world.cell_size, i*world.cell_size, world.cell_size, world.cell_size), 0)
    pygame.display.update()
    print "frame "+str(frame_count)
    frame_count += 1

pygame.display.quit()
pygame.quit()
