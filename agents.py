
class car(object):
    """docstring for car"""
    def __init__(self, num, dir, x, y, dx, dy):
        super(car, self).__init__()
        self.num = num # id
        self.dx = dx
        self.dy = dy 
        self.x = x 
        self.y = y
        self.history = [(x - dx, y - dy), (x - 2*dx, y - 2*dy), (x - 3*dx, y - 3*dy)]
        self.path = [(x + dx, y + dy), (x - 2*dx, y - 2*dy), (x - 3*dx, y - 3*dy)]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy 


class signal(object):
    """docstring for signal"""
    def __init__(self, arg):
        super(signal, self).__init__()
        self.arg = arg
        