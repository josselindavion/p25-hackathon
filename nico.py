
from constantes import(GRID_SIZE, INITIAL_SHEEP, INITIAL_WOLVES, MAX_TURNS, SHEEP_INITIAL_ENERGY, WOLF_INITIAL_ENERGY,
                      SHEEP_ENERGY_FROM_GRASS, WOLF_ENERGY_FROM_SHEEP, WOLF_ENERGY_LOSS_PER_TURN, SHEEP_ENERGY_LOSS_PER_TURN,
                      SHEEP_REPRODUCTION_THRESHOLD, WOLF_REPRODUCTION_THRESHOLD, REPRODUCTION_ENERGY_COST,
                      SHEEP_MAX_AGE, WOLF_MAX_AGE, GRASS_GROWTH_PROBABILITY, GRASS_REGROWTH_TIME)

import numpy as np

class Wolf:

    #paramètres initiales de la classe.
    def __init__(self, id: int, position: tuple, energy: int, age: int, alive: bool):
        self.id = id
        self.position = position
        self.energy = energy
        self.age = age
        self.alive = alive

    def __repr__(self):
        return f"Wolf(id={self.id}, position=({self.position}), energy={self.energy}, age={self.age})"
    
    #prend 1 an en plus au bout d'un tour
    def aging_wolf(self):
        self.age += 1

    #déplace le loup à une nouvelle position
    def deplace(self, new_position):
        self.position = new_position

    #augmente/diminue le niveau d'énergie du loup
    def energy_gain(self, energy_gain: int):
        self.energy += energy_gain

    # Méthode pour savoir si le loup est en vie
    def is_alive(self):
        if self.energy <= 0 or WOLF_MAX_AGE >= self.age: #WOLF_MAX_AGE sera défini quelque part dans le code principal
            self.alive = False
    



