import numpy as np

EMPTY = 0
CAR = 1
PEDESTRIAN = 2
WALL = 3
COLL = 4

COLORS = {EMPTY:(0,0,0), CAR:(255, 255, 255), COLL:(255,0,0), WALL:(0,255,0)}


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


    def update(self):
        pass



        