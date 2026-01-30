from nico import Wolf
import numpy as np
from constantes import(GRID_SIZE, INITIAL_SHEEP, INITIAL_WOLVES, MAX_TURNS, SHEEP_INITIAL_ENERGY, WOLF_INITIAL_ENERGY,
                      SHEEP_ENERGY_FROM_GRASS, WOLF_ENERGY_FROM_SHEEP, WOLF_ENERGY_LOSS_PER_TURN, SHEEP_ENERGY_LOSS_PER_TURN,
                      SHEEP_REPRODUCTION_THRESHOLD, WOLF_REPRODUCTION_THRESHOLD, REPRODUCTION_ENERGY_COST,
                      SHEEP_MAX_AGE, WOLF_MAX_AGE, GRASS_GROWTH_PROBABILITY, GRASS_REGROWTH_TIME, INITIAL_GRASS_COVERAGE)
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
    ## On fait un grow_back à chaque tour à toutes les cellules ##
    def grow_back(self):
        self.age += 1
        if self.age >= GRASS_REGROWTH_TIME:
            self.alive = True

    def die(self):
        self.alive = False
        self.age = 0

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
        ## Il faut avoir de la grass alive sur un pourcentage INITIAL_GRASS_COVERAGE ##
        ## L'age de chaque herbe est initialisé random entre 0 et GRASS_REGROWTH_TIME ##
        total_cells = self.width * self.height
        initial_grass_count = int(total_cells * INITIAL_GRASS_COVERAGE)
        while len([grass for grass in self.list_grass if grass.alive]) < initial_grass_count:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            ## Eviter de créer plusieurs herbes au même endroit ##
            position_occupied = any(grass.position == (x,y) for grass in self.list_grass)
            if not position_occupied:
                new_grass = Grass(position=(x,y), age=np.random.randint(0, GRASS_REGROWTH_TIME), alive=True)
                self.list_grass.append(new_grass)
        
        # Mettre de la grass morte sur le reste des cases
        for x in range(self.width):
            for y in range(self.height):
                position_occupied = any(grass.position == (x,y) for grass in self.list_grass)
                if not position_occupied:
                    new_grass = Grass(position=(x,y), age=0, alive=False)
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
    
    ## Méthode pour afficher la grille ##
    def display_grid(self):
        grid = [[[0,0] for _ in range(self.width)] for _ in range(self.height)]
        for sheep in self.list_sheep:
            x, y = sheep.position
            grid[y][x][1]= 'S'
        for wolf in self.list_wolf:
            x, y = wolf.position
            grid[y][x][1] = 'W'
        for grass in self.list_grass:
            if grass.alive:
                x, y = grass.position
                grid[y][x][0]= 'G'
            else:
                x, y = grass.position
                grid[y][x][0] = 'g'
        for row in grid:
            print(' | '.join([f"{cell[0]}{cell[1]}" for cell in row]))
        print("\n")
   
    ## evolve renvoi False si la simulation doit s'arrêter ##
    def evolve(self)-> bool:
        
        ## INCREMENTATION AGE DE TOUS LES ANIMAUX ##
        for sheep in self.list_sheep:
            sheep.aging_sheep()
        for wolf in self.list_wolf:
            wolf.aging_wolf()
        
        ## INCREMENTATION AGE DE TOUTE L'HERBE ##
        for grass in self.list_grass:
            if not grass.alive:
                grass.grow_back()
        
        
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
                    sheep.energy_gain(SHEEP_ENERGY_FROM_GRASS)
                    grass.die()  ## L'herbe meurt après avoir été mangée ##
                    break  ## Sortir de la boucle une fois l'herbe trouvée et mangée ##

        ## PHASE LOUPS ##
        for wolf in self.list_wolf:

            ## Si il y a un mouton sur une case adjcente, le loup se déplace dessus et mange le mouton ##
            x, y = wolf.position
            ## Trouver les positions adjacentes dans la grille sans modulo ##
            adjacent_positions = [ (x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] 
                                   if 0 <= x+dx < self.width and 0 <= y+dy < self.height ]
            ## On regarde si il y a des moutons sur ces positions ##
            sheep_positions = [pos for pos in adjacent_positions 
                               if any(sheep.position == pos for sheep in self.list_sheep)]
            if sheep_positions:
                new_position = sheep_positions[0]  ## Prendre la première position avec un mouton ##
                wolf.deplace(new_position)
                ## Manger le mouton ##
                for sheep in self.list_sheep:
                    if sheep.position == new_position:
                        wolf.energy_gain(WOLF_ENERGY_FROM_SHEEP)
                        sheep.alive = False  ## Le mouton est tué ##
                        break  ## Sortir de la boucle une fois le mouton trouvé et mangé ##

            else:
                ## Sinon le loup se déplace aléatoirement sur une case adjacente ##
                if adjacent_positions:
                    new_position = adjacent_positions[np.random.randint(0, len(adjacent_positions))]
                    wolf.deplace(new_position)
            
            ## Tous les moutons adjacents au loup après son déplacement sont mangés ##
            for sheep in self.list_sheep.copy():
                if sheep.position in adjacent_positions:
                    wolf.energy_gain(WOLF_ENERGY_FROM_SHEEP)
                    sheep.alive = False  ## Le mouton est tué ##
            
            ## NB : le loup perd de l'energie en se déplaçant (déjà géré dans la méthode deplace) ##

            
        ## SUPPRESSION DES MOUTONS MORTS ##
        for sheep in self.list_sheep.copy():
            if not sheep.alive:
                self.list_sheep.remove(sheep)
        
        ## SUPPRESSION DES LOUPS MORTS ##
        for wolf in self.list_wolf.copy():
            if not wolf.alive:
                self.list_wolf.remove(wolf)
        
        ## GESTION DE LA REPRODUCTION - MOUTONS ##
        ## On vérifie pour chaque mouton s'il peut se reproduire (energie supérieur au seuil) et on crée un nouveau mouton ##
        ## Le nouveau mouton est placé sur une case adjacente vide aléatoirement ##
        ## Si aucune case adjacente n'est libre, pas de reproduction ##
        for sheep in self.list_sheep.copy():
            if sheep.energy >= SHEEP_REPRODUCTION_THRESHOLD:
                x, y = sheep.position
                adjacent_positions = [ (x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] 
                                       if 0 <= x+dx < self.width and 0 <= y+dy < self.height ]
                free_positions = [pos for pos in adjacent_positions 
                                  if not any(s.position == pos for s in self.list_sheep)]
                if free_positions:
                    new_position = free_positions[0] ## Prendre la première position libre ##
                    new_sheep = Sheep(id=len(self.list_sheep), position=new_position, energy=SHEEP_INITIAL_ENERGY, age=0, alive=True)
                    self.add_sheep(new_sheep)
                    sheep.energy -= REPRODUCTION_ENERGY_COST  ## Coût énergétique de la reproduction ##
        
        ## GESTION DE LA REPRODUCTION - LOUPS ##
        for wolf in self.list_wolf.copy():
            if wolf.energy >= WOLF_REPRODUCTION_THRESHOLD:
                x, y = wolf.position
                adjacent_positions = [ (x+dx, y+dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)] 
                                       if 0 <= x+dx < self.width and 0 <= y+dy < self.height ]
                free_positions = [pos for pos in adjacent_positions 
                                  if not any(w.position == pos for w in self.list_wolf)]
                if free_positions:
                    new_position = free_positions[0] ## Prendre la première position libre ##
                    new_wolf = Wolf(id=len(self.list_wolf), position=new_position, energy=WOLF_INITIAL_ENERGY, age=0, alive=True)
                    self.add_wolf(new_wolf)
                    wolf.energy -= REPRODUCTION_ENERGY_COST  ## Coût énergétique de la reproduction ##

        ## AFFICHAGE DE L'ÉTAT ACTUEL DE LA GRILLE ##
        self.display_grid()

        ## VERIFICATION CONDITIONS DE FIN DE LA SIMULATION ##
        ##  Condition 1 : Plus de moutons ##
        if len(self.list_sheep) == 0:
            print("Simulation ends: All sheep are dead.")
            return False
        ##  Condition 2 : Plus de loups ##
        if len(self.list_wolf) == 0:
            print("Simulation ends: All wolves are dead.")
            return False
        return True