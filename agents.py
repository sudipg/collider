import random

CAR_OBEYED = 0
CAR_JUMPED = 1
CAR_DECIDING = 2

class car(object):
    """docstring for car"""
    def __init__(self, dir, x, y, dx, dy):
        super(car, self).__init__()
        self.dir = dir # 1 for EW         0 for NS
        self.dx = dx
        self.dy = dy 
        self.x = x 
        self.y = y
        self.history = [(x - dx, y - dy), (x - 2*dx, y - 2*dy), (x - 3*dx, y - 3*dy)]
        self.path = [(x + dx, y + dy), (x - 2*dx, y - 2*dy), (x - 3*dx, y - 3*dy)]
        self.jumped_light = CAR_DECIDING

    def generate_path(self, x, y , dx, dy):
        return [(x+i*dx, y+i*dy) for i in range(3)]

    def move(self):
        self.history = self.history[1:] + [(self.x, self.y)]
        self.path = self.generate_path(self.x, self.y, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy

    def stop(self):
        self.dx = 0
        self.dy = 0

    def start(self):
        self.dx = self.dir
        self.dy = (1-self.dir)