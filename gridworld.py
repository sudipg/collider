import numpy as np
import random
from agents import *

EMPTY = 0
CAR = 1
PEDESTRIAN = 2
WALL = 3
COLL = 4

COLORS = {EMPTY:(0,0,0), CAR:(255, 255, 255), COLL:(255,0,0), WALL:(50,100,50)}

 
SIGNAL_EW = 0
SIGNAL_NS = 1
SIGNAL_YELLOW = 2
SIGNAL_INT = {SIGNAL_EW:30, SIGNAL_YELLOW:10, SIGNAL_NS:30} #ticks starts as EW
SIGNAL_SEQ = [SIGNAL_EW, SIGNAL_YELLOW, SIGNAL_NS, SIGNAL_YELLOW]
NUM_CARS = 20
SPAWN_CHANCE = 0.1
DRIVER_STUPIDITY = 0.05 # chance of jumping red 

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
        self.signal_count = 0
        self.time_on_signal = 0
        self.signal_trigger = True

    def update_signal(self):
        if self.time_on_signal < SIGNAL_INT[self.signal]:
            self.time_on_signal += 1
            if self.time_on_signal > 1:
                self.signal_trigger = False
        else:
            self.signal_trigger = True
            self.signal_count += 1
            self.time_on_signal = 0
            self.signal = SIGNAL_SEQ[self.signal_count%4]

    def update(self):
        """ One tick of the grid world. """
        self.ticks += 1
        # signal first
        self.update_signal()

        if len(self.cars) < NUM_CARS:
            self.spawn_car()

        new_cars = []

        for car in self.cars:
            if self.signal_trigger and SIGNAL_SEQ[(self.signal_count-1)%4] == SIGNAL_YELLOW:
                car.start()
            # follow rules! execute on light change only 
            if self.signal == SIGNAL_YELLOW: # special rules for yellow light - clear intersection only.
                if car.dir == 0 and car.y < self.road_y_start:
                    car.stop()
                if car.dir == 1 and car.x < self.road_x_start:
                    car.stop()
            else:
                if car.dx == 0 and car.dy == 0:
                    if car.dir == 1 and self.signal == SIGNAL_EW:
                        car.start()
                    elif car.dir == 0 and self.signal == SIGNAL_NS:
                        car.start()
                elif car.dx > 0 and self.signal == SIGNAL_NS and car.x < self.road_x_end:
                    if car.jumped_light == CAR_DECIDING:
                        if not self.car_see_empty(car):
                            car.stop()
                            car.jumped_light = CAR_OBEYED
                        elif car.x == self.road_x_start-1:
                            if random.random() > DRIVER_STUPIDITY:
                                car.stop()
                                car.jumped_light = CAR_OBEYED
                            else:
                                car.jumped_light = CAR_JUMPED
                        else:
                            car.jumped_light = CAR_DECIDING
                    elif car.jumped_light == CAR_OBEYED:
                        car.stop()
                elif car.dy > 0 and self.signal == SIGNAL_EW and car.y < self.road_y_end:
                    if car.jumped_light == CAR_DECIDING:
                        if not self.car_see_empty(car):
                                car.stop()
                                car.jumped_light = CAR_OBEYED
                        elif car.y == self.road_y_start - 1:
                            if random.random() > DRIVER_STUPIDITY:
                                car.stop()
                                car.jumped_light = CAR_OBEYED
                            else:
                                car.jumped_light = CAR_JUMPED
                        else:
                            car.jumped_light = CAR_DECIDING  
                    elif car.jumped_light == CAR_OBEYED:
                        car.stop()
            if car.x < self.width and car.y < self.height:
                self.cells[car.y][car.x].item = EMPTY
                car.move()
                if car.x < self.width and car.y < self.height:
                    self.cells[car.y][car.x].item = CAR
                    new_cars.append(car)

        self.cars = new_cars

    def car_see_empty(self, car, rnge = 3):
        if car.dir == 1:
            for x in range(car.x+1, car.x+rnge):
                if self.cells[car.y][x].item == CAR:
                    return False
            return True
        else:
            for y in range(car.y+1, car.y+rnge):
                if self.cells[y][car.x].item == CAR:
                    return False
            return True

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