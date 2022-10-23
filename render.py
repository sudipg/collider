import pygame
import time
import sys
import numpy as np
from agents import *
from gridworld import *

pygame.init()
stupidity = float(input("Enter driver stupidity: "))
world = grid_world(20,20,20, stupidity) 


screen = pygame.display.set_mode((world.height * world.cell_size, world.height * world.cell_size))

frame_count = 0
TIME_PER_FRAME = 0.01

pygame.font.init()
rec_font = pygame.font.SysFont('Comic Sans MS', 20)
crashes = 0
prev_crash = None

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
    world.update()
    collision = world.detect_collisions()
    time.sleep(TIME_PER_FRAME)
    screen.fill(EMPTY)
    for i in range(world.height):
        for j in range(world.width):
            pygame.draw.rect(screen, COLORS[world.cells[i][j].item], (j*world.cell_size, i*world.cell_size, world.cell_size, world.cell_size), 0)
    
    # render cars
    for car in world.cars:
        pygame.draw.rect(screen, COLORS[CAR], (world.cell_size*car.x, world.cell_size*car.y, world.cell_size, world.cell_size), 0)


    signal_EW = (255, 0, 0) if world.signal == SIGNAL_NS else (0,255, 0)
    signal_NS = (255, 0, 0) if world.signal == SIGNAL_EW else (0,255, 0)
    
    if world.signal == SIGNAL_YELLOW:
        signal_NS = (255,255,0)
        signal_EW = (255,255,0)

    if collision:
        pygame.draw.rect(screen, (255, 0, 0), (collision[0] * world.cell_size, collision[1] * world.cell_size, world.cell_size, world.cell_size), 0)        
        print("crash!")
        if collision != prev_crash:
            crashes += 1


    pygame.draw.circle(screen, signal_NS, (world.cell_size*2*world.width/10, world.cell_size*2*world.height/10), world.cell_size/2, 0)
    pygame.draw.circle(screen, signal_EW, (world.cell_size*8*world.width/10, world.cell_size*8*world.height/10), world.cell_size/2, 0)
    fc = rec_font.render(" t="+str(frame_count), False, (0, 0, 0))
    cc = rec_font.render("crashes="+str(crashes), False, (0, 0, 0))
    screen.blit(fc,(0,0))
    screen.blit(cc,(0,22))
    pygame.display.update()
    if collision:
        time.sleep(1)
    print("frame "+str(frame_count))
    print(world.cars)
    frame_count += 1
    prev_crash = collision

pygame.display.quit()
pygame.quit()
