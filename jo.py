
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
        self.energy -= 1  ## Déplacement coûte de l'énergie
    
    ## Méthode pour actualiser l'énergie du mouton #
    def energy_gain(self, energy_gain:int):
        self.energy += energy_gain
    
    ## Méthode pour tuer le mouton ##
    def isalive(self):
        if self.energy <= 0 or self.age >= SHEEP_MAX_AGE:
            self.alive = False