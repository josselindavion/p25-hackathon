## Importation des classes ##
import numpy as np
from nico import Wolf
from jo import Sheep, Grass, Grid


def main():
    ## Initialisation de la grille ##
    grid = Grid(GRID_SIZE[0], GRID_SIZE[1])
    grid.initialisation(INITIAL_SHEEP, INITIAL_WOLVES)
    for tour in range(MAX_TURNS):
        print(f"Tour {tour + 1}")
        grid.evolve() 
    print("Simulation terminée.")
