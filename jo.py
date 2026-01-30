
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
    ## On fait un grow_back à chaque tour sur celles qui sont mortes ##
    def grow_back(self):
        self.age += 1
        if self.age >= GRASS_GROWTH_TIME:
            self.alive = True
            self.age = 0

    def die(self):
        self.alive = False