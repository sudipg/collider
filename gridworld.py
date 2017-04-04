import numpy as np
from agents import *

EMPTY = 0
CAR = 1
PEDESTRIAN = 2
WALL = 3
COLL = 4

COLORS = {EMPTY:(0,0,0), CAR:(255, 255, 255), COLL:(255,0,0), WALL:(50,100,50)}

SIGNAL_INT = 100 #ticks starts as EW 
SIGNAL_EW = 0
SIGNAL_NS = 1
NUM_CARS = 20

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
        


    def detect_collisions(self):
        """ return the x,y coord of the collision else None"""

    