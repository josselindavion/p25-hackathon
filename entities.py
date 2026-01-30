## CLASSE DES ENTITES ##

from constantes import(GRID_SIZE, INITIAL_SHEEP, INITIAL_WOLVES, MAX_TURNS, SHEEP_INITIAL_ENERGY, WOLF_INITIAL_ENERGY,
                      SHEEP_ENERGY_FROM_GRASS, WOLF_ENERGY_FROM_SHEEP, WOLF_ENERGY_LOSS_PER_TURN, SHEEP_ENERGY_LOSS_PER_TURN,
                      SHEEP_REPRODUCTION_THRESHOLD, WOLF_REPRODUCTION_THRESHOLD, REPRODUCTION_ENERGY_COST,
                      SHEEP_MAX_AGE, WOLF_MAX_AGE, GRASS_GROWTH_PROBABILITY, GRASS_REGROWTH_TIME,INITIAL_GRASS_COVERAGE)
import numpy as np

## CLASSE DU MOUTON ##
class Sheep:
    
    ## Méthode d'initialisation de la classe Sheep ##
    def __init__(self, id:int, position:tuple, energy:int, age:int, alive:bool):
        self.id = id
        self.position = position
        self.energy = energy
        self.age = age
        self.alive = alive
    
    ## Méthode pour afficher les informations de l'objet Sheep ##
    def __repr__(self):
        return f'Sheep(id={self.id}, position={self.position}, energy={self.energy}, age={self.age})'
    
    ## Méthode pour faire vieillir le mouton au bout d'un tour ##
    def aging_sheep(self):
        self.age += 1
    
    ## Méthode pour actualiser la position du mouton ##
    def deplace(self, new_position:tuple):
        self.position = new_position
        self.energy -= SHEEP_ENERGY_LOSS_PER_TURN  ## Déplacement coûte de l'énergie
    
    ## Méthode pour actualiser l'énergie du mouton #
    def energy_gain(self, energy_gain:int):
        self.energy += energy_gain
    
    ## Méthode pour tuer le mouton ##
    def is_alive(self):
        if self.energy <= 0 or self.age >= SHEEP_MAX_AGE:
            self.alive = False


## CLASSE DE L'HERBE ##
class Grass:

    ## Méthode d'initialisation de la classe Grass ##
    def __init__(self, position:tuple, age:int, alive:bool):
        self.age = age
        self.position = position
        self.alive = alive
    
    ## Méthode pour afficher les informations de l'objet Grass ##
    def __repr__(self):
        return f'Grass(position={self.position}, age={self.age}, alive={self.alive})'
    
    ## Méthode du temps de repousse ##
    ## On fait un grow_back à chaque tour à toutes les cellules ##
    def grow_back(self):
        self.age += 1
        if self.age >= GRASS_REGROWTH_TIME:
            self.alive = True

    def die(self):
        self.alive = False
        self.age = 0


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
        self.energy -= WOLF_ENERGY_LOSS_PER_TURN  # Perte d'énergie à chaque déplacement

    #augmente/diminue le niveau d'énergie du loup
    def energy_gain(self, energy_gain: int):
        self.energy += energy_gain

    # Méthode pour savoir si le loup est en vie
    def is_alive(self):
        if self.energy <= 0 or WOLF_MAX_AGE >= self.age: #WOLF_MAX_AGE sera défini quelque part dans le code principal
            self.alive = False