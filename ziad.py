
from jo import Ship
from nico import Wolf



class Grid() : 

    def __init__(self, width, height) :
        self.width = width
        self.height = height
        self.grid = [ [ [ None , None ] for x in range(width) ] for y in range(height) ]

    def set(self, x, y, value) :
        self.grid[y][x] = value

    def get(self, x, y) :
        return self.grid[y][x]
    

