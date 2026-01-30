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

## CLASSE DE LA GRILLE ##
class Grid:

    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.list_sheep = []
        self.list_grass = []
        self.list_wolf = []
    
    def add_sheep(self, sheep:Sheep):
        self.list_sheep.append(sheep)
    
    def add_wolf(self, wolf:Wolf):
        self.list_wolf.append(wolf)
    
    
    ## Initialisation des moutons et de l'herbe sur la grille ##
    def initialisation(self, initial_sheep:int, initial_wolf:int):
        while len(self.list_sheep) < initial_sheep:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            ## Eviter de créer plusieurs moutons au même endroit ##
            position_occupied = any(sheep.position == (x,y) for sheep in self.list_sheep)
            if not position_occupied:
                new_sheep = Sheep(id=len(self.list_sheep), position=(x,y), energy=SHEEP_INITIAL_ENERGY, age=0, alive=True)
                self.add_sheep(new_sheep)

        ## Initialisation de l'herbe sur la grille ##
        ## Il faut avoir de la grass alive partout au début ##
        for x in range(self.width):
            for y in range(self.height):
                new_grass = Grass(position=(x,y), age=0, alive=True)
                self.list_grass.append(new_grass)
                
        while len(self.list_wolf) < initial_wolf:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            ## Eviter de créer plusieurs loups au même endroit ##
            ## Eviter de créer des loups ou ya des moutons ##
            position_occupied_by_wolf = any(wolf.position == (x,y) for wolf in self.list_wolf)
            position_occupied_by_sheep = any(sheep.position == (x,y) for sheep in self.list_sheep)
            position_occupied = position_occupied_by_wolf or position_occupied_by_sheep
            if not position_occupied:
                new_wolf = Wolf(id=len(self.list_wolf), position=(x,y), energy=WOLF_INITIAL_ENERGY, age=0, alive=True)
                self.add_wolf(new_wolf)
    
    
    
    def evolve(self):
        
        ## INCREMENTATION AGE DE TOUS LES ANIMAUX ##
        for sheep in self.list_sheep:
            sheep.aging_sheep()
        for wolf in self.list_wolf:
            wolf.aging_wolf()
        
        ## INCREMENTATION AGE DE TOUTE L'HERBE ##
        for grass in self.list_grass:
            if not grass.alive:
                grass.grow_back()
        

        ## SUPPRESSION DES MOUTONS MORTS ##
        for sheep in self.list_sheep.copy():
            if not sheep.alive:
                self.list_sheep.remove(sheep)
        
        ## SUPPRESSION DES LOUPS MORTS ##
        for wolf in self.list_wolf.copy():
            if not wolf.alive:
                self.list_wolf.remove(wolf)
        
        ## PHASE MOUTONS ##
        for sheep in self.list_sheep:

            ## Si il y a de l'herbe vivante sur une case adjcente, le mouton se déplace dessus et mange l'herbe ##
            x, y = sheep.position
            ## Trouver les positions adjacentes dans la grille sans modulo ##
            adjacent_positions = [ (x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] 
                                   if 0 <= x+dx < self.width and 0 <= y+dy < self.height ]
            ## On regarde si il y a de l'herbe vivante sur ces positions ##
            grass_positions = [pos for pos in adjacent_positions 
                               if any(grass.position == pos and grass.alive for grass in self.list_grass)]
            if grass_positions:
                new_position = grass_positions[0]  ## Prendre la première position avec de l'herbe ##
                sheep.deplace(new_position)
            ## Pour l'herbe mangée, on fera un check à la fin de la phase mouton ##

            else:
                ## Sinon le mouton se déplace aléatoirement sur une case adjacente ##
                if adjacent_positions:
                    new_position = adjacent_positions[np.random.randint(0, len(adjacent_positions))]
                    sheep.deplace(new_position)
            
            ## NB : le mouton perd de l'energie en se déplaçant (déjà géré dans la méthode deplace) ##
            ## Alimentation du mouton si il y a de l'herbe vivante sur sa position ##
            for grass in self.list_grass:
                if grass.position == sheep.position and grass.alive:
                    sheep.energy_gain(SHEEP_ENERGY_GAIN)
                    grass.die()  ## L'herbe meurt après avoir été mangée ##
                    break  ## Sortir de la boucle une fois l'herbe trouvée et mangée ##
