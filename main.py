## Importation des classes ##
import numpy as np
from nico import Wolf
from jo import Sheep, Grass, Grid

## Paramètres de la simulation ##

# Configuration initiale

GRID_SIZE = (20, 20)  # Taille de la grille (largeur, hauteur)
INITIAL_SHEEP = 10   # Nombre initial de moutons
INITIAL_WOLVES = 10   # Nombre initial de loups
INITIAL_GLASS_COVERAGE = 0.3  # Pourcentage initial de couverture végétale

SHEEP_INITIAL_ENERGY = 20
WOLF_INITIAL_ENERGY = 40
SHEEP_ENERGY_FROM_GRASS = 10
WOLF_ENERGY_FROM_SHEEP = 20
WOLF_ENERGY_LOSS_PER_TURN = 2
SHEEP_ENERGY_LOSS_PER_TURN = 1

# --- Paramètres de Reproduction ---
SHEEP_REPRODUCTION_THRESHOLD = 50
WOLF_REPRODUCTION_THRESHOLD = 80
REPRODUCTION_ENERGY_COST = 20

# --- Paramètres d'Âge ---
SHEEP_MAX_AGE = 50  # Tours avant mort naturelle
WOLF_MAX_AGE = 40

# --- Paramètres de l'Herbe ---
GRASS_GROWTH_PROBABILITY = 0.08
GRASS_REGROWTH_TIME = 7

# --- Paramètres de la Simulation ---
MAX_TURNS = 500  # Nombre maximum de tours

