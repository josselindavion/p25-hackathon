
## CLASSE DU MOUTON ##
class Sheep:
    
    ## Méthode d'initialisation de la classe Sheep ##
    def __init__(self, id:int, position:tuple, energy:int, age:int):
        self.id = id
        self.position = position
        self.energy = energy
        self.age = age
    
    ## Méthode pour afficher les informations de l'objet Sheep ##
    def __repr__(self):
        return f'Sheep(id={self.id}, position={self.position}, energy={self.energy}, age={self.age})'
    
    ## Méthode pour faire vieillir le mouton au bout d'un tour ##
    def aging_sheep(self):
        self.age += 1
    
    def deplace(self, new_position:tuple):
        self.position = new_position