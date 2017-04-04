import pygame
import time
import sys
import numpy as np
from gridworld import *

pygame.init()
world = grid_world(20,20,20) 

screen = pygame.display.set_mode((world.height * world.cell_size, world.height * world.cell_size))

frame_count = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
    world.update()
    collision = world.detect_collisions()
    time.sleep(1.0/60)
    screen.fill(EMPTY)
    for i in range(world.height):
        for j in range(world.width):
            pygame.draw.rect(screen, COLORS[world.cells[i][j].item], (j*world.cell_size, i*world.cell_size, world.cell_size, world.cell_size), 0)
    
    signal_EW = (255, 0, 0) if world.signal == SIGNAL_NS else (0,255, 0)
    signal_NS = (255, 0, 0) if world.signal == SIGNAL_EW else (0,255, 0)
    pygame.draw.circle(screen, signal_NS, (world.cell_size*2*world.width/10, world.cell_size*2*world.height/10), world.cell_size/2, 0)
    pygame.draw.circle(screen, signal_EW, (world.cell_size*8*world.width/10, world.cell_size*8*world.height/10), world.cell_size/2, 0)
    pygame.display.update()
    print "frame "+str(frame_count)
    frame_count += 1

pygame.display.quit()
pygame.quit()
