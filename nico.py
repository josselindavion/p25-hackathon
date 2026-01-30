class Wolf:
    #paramètres initiales de la classe.
    def __init__(self, id: int, position: tuple, energy: int, age: int):
        self.id = id
        self.position = position
        self.energy_level = energy
        self.age = age

    def __repr__(self):
        return f"Wolf(id={self.id}, position=({self.x}, {self.y}), energy_level={self.energy_level}, age={self.age})"
    
    #prend 1 an en plus au bout d'un tour
    def aging_wolf(self):
        self.age += 1

    def deplace(self, new_position):
        self.position = new_position


w = Wolf(1, (10, 20), 100, 5)
print(w)  

