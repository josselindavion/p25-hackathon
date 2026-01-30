## Importation des classes ##
import numpy as np
from nico import Wolf
from jo import Sheep, Grass, Grid
from constantes import(GRID_SIZE, INITIAL_SHEEP, INITIAL_WOLVES, MAX_TURNS, SHEEP_INITIAL_ENERGY, WOLF_INITIAL_ENERGY,
                      SHEEP_ENERGY_FROM_GRASS, WOLF_ENERGY_FROM_SHEEP, WOLF_ENERGY_LOSS_PER_TURN, SHEEP_ENERGY_LOSS_PER_TURN,
                      SHEEP_REPRODUCTION_THRESHOLD, WOLF_REPRODUCTION_THRESHOLD, REPRODUCTION_ENERGY_COST,
                      SHEEP_MAX_AGE, WOLF_MAX_AGE, GRASS_GROWTH_PROBABILITY, GRASS_REGROWTH_TIME)

def main():
    ## Initialisation de la grille ##
    grid = Grid(GRID_SIZE[0], GRID_SIZE[1])
    grid.initialisation(INITIAL_SHEEP, INITIAL_WOLVES)
    grid.display_grid()
    for tour in range(MAX_TURNS):
        print(f"Tour {tour + 1}")
        grid.evolve() 
    print("Simulation terminée.")

main()
