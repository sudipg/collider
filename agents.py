
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

    def generate_path(x, y , dx, dy):
        return [(x+i*dx, y+i*dy) for i in range(3)]

    def move(self, dx, dy):
        self.history = self.history[1:] + [(self.x, self.y)]
        self.path = generate_path(self.x, self.y)
        self.x += dx
        self.y += dy 
        self.history = self.history[1:]
        self.path = self.path[:-1]

