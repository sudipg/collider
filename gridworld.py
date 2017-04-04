import numpy as np
import random
from agents import *

EMPTY = 0
CAR = 1
PEDESTRIAN = 2
WALL = 3
COLL = 4

COLORS = {EMPTY:(0,0,0), CAR:(255, 255, 255), COLL:(255,0,0), WALL:(50,100,50)}

SIGNAL_INT = 10 #ticks starts as EW 
SIGNAL_EW = 0
SIGNAL_NS = 1
NUM_CARS = 20
SPAWN_CHANCE = 0.1

class cell(object):
    """docstring for cell"""
    def __init__(self, x, y, item = None):
        super(cell, self).__init__()
        self.x = x
        self.y = y
        self.item = item
        

class grid_world(object):
    """docstring for grid_world"""
    
    def __init__(self, width = 100, height = 100, cell_size = 5):
        super(grid_world, self).__init__()
        self.ticks = 0
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [[cell(i, j, WALL) for j in range(width)] for i in range(height)]

        self.road_x_start = width / 3
        self.road_x_end = width - width / 3
        self.road_y_start = height / 3
        self.road_y_end = height - height / 3
        self.y_crossing = self.road_y_start - 1
        self.x_crossing = self.road_x_start - 1


        for i in range(self.road_y_start, self.road_y_end):
            for j in range(width):
                self.cells[i][j].item = EMPTY
        for j in range(self.road_x_start, self.road_x_end):
            for i in range(height):
                self.cells[i][j].item = EMPTY

        self.signal = SIGNAL_EW 
        self.cars = []
        self.collision_map = np.zeros((height, width))

    def update(self):
        """ One tick of the grid world. """
        self.ticks += 1
        # signal first
        self.signal = SIGNAL_EW if (self.ticks / SIGNAL_INT) % 2 == 0 else SIGNAL_NS

        if len(self.cars) < NUM_CARS:
            self.spawn_car()

        new_cars = []

        for car in self.cars:
            # follow rules! 
            if car.dx == 0 and car.dy == 0:
                if car.dir == 1 and self.signal == SIGNAL_EW:
                    car.start()
                elif car.dir == 0 and self.signal == SIGNAL_NS:
                    car.start()
            elif car.dx > 0 and self.signal == SIGNAL_NS:
                car.stop()
            elif car.dy > 0 and self.signal == SIGNAL_EW:
                car.stop()
            if car.x < self.width and car.y < self.height:
                self.cells[car.y][car.x].item = EMPTY
                car.move()
                if car.x < self.width and car.y < self.height:
                    self.cells[car.y][car.x].item = CAR
                    new_cars.append(car)

        self.cars = new_cars


    def detect_collisions(self):
        """ return the x,y coord of the collision else None"""
        for t in range(3):
            self.collision_map = np.zeros((self.height, self.width))
            for car in self.cars:
                # check if in bounds:
                if car.path[t][0] >= self.width or car.path[t][1] >= self.height:
                    continue

                if self.collision_map[car.path[t]] == 1:
                    return car.path[t]
                else:
                    self.collision_map[car.path[t]] = 1

        return None

    def spawn_car(self):
        # pick a spot to spawn:
        new_car = None
        if np.random.choice((0,1)): # NS
            for x in range(self.road_x_start, self.road_x_end):
                if random.random() < SPAWN_CHANCE and self.cells[0][x].item == EMPTY:
                    new_car = car(0, x, 0, 0, 1)
        else: # EW
            for y in range(self.road_y_start, self.road_y_end):
                if random.random() < SPAWN_CHANCE and self.cells[y][0].item == EMPTY:
                    new_car = car(1, 0, y, 1, 0)
            
        if new_car:
            self.cars.append(new_car)
            self.cells[new_car.y][new_car.x].item = CAR