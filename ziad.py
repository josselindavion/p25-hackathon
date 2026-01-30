import numpy as np


SHEEP_INITIAL_ENERGY = 20
WOLF_INITIAL_ENERGY = 40



class Grid() : 

    def __init__(self, width, height, initial_sheep , initial_wolves, initial_grass) :

        self.width = width
        self.height = height
        self.grid = [ [ ( None , None) for x in range(width) ] for y in range(height) ]

        for i in range(initial_sheep ):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)

            current_grass, current_entity = self.get(x, y)

            self.set(x, y, (current_grass, "S") )

        for j in range(initial_wolves):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)

            current_grass, current_entity = self.get(x, y)
            self.set(x, y, ( current_grass , "W") )

        for k in range(initial_grass): 
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)

            current_grass, current_entity = self.get(x, y)
            self.set(x, y, (1 , current_entity) )
        

    def set(self, x, y, value) :
        self.grid[y][x] = value

    def get(self, x, y) :
        return self.grid[y][x]
    
    def __repr__(self) :
        representation = ""
        for row in self.grid :
            representation += " | ".join( f"{cell[0]},{cell[1]}" for cell in row ) + "\n"
        return representation
# Exemple d'utilisation

    