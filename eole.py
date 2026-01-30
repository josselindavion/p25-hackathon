import pygame
import sys
import random

#Paramètres d'affichage
TAILLE_CASE = 20          
COULEUR_TERRE = (139, 69, 19)    # Marron (Sol vide)
COULEUR_HERBE = (34, 139, 34)    # Vert (Herbe)
COULEUR_MOUTON = (255, 255, 255) # Blanc (Mouton)
COULEUR_LOUP = (0, 0, 0)     # Noir (Loup)
COULEUR_GRILLE = (50, 50, 50)    # Gris foncé (Lignes de séparation)

class Afficheur:
    def __init__(self, grille_exemple):

        pygame.init()
        
        # Calcul automatique de la taille de la fenêtre selon la grille reçue
        self.hauteur_grille = len(grille_exemple)
        self.largeur_grille = len(grille_exemple[0])
        
        largeur_fenetre = self.largeur_grille * TAILLE_CASE
        hauteur_fenetre = self.hauteur_grille * TAILLE_CASE
        
        self.ecran = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
        pygame.display.set_caption("Simulation Ecosystème")

    def update(self, grille):


        #Fermeture de la fenêtre 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        for y in range(self.hauteur_grille):
            for x in range(self.largeur_grille):
                
                # Récupération des données
                herbe_presente, entite = grille[y][x]
                
                # Définition du carré (le fond)
                rect = (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                
                
                if herbe_presente == 1 or entite == '#':
                    pygame.draw.rect(self.ecran, COULEUR_HERBE, rect)
                else:
                    pygame.draw.rect(self.ecran, COULEUR_TERRE, rect)
                
                #On dessine l'animal avec un rond
                centre = (x * TAILLE_CASE + TAILLE_CASE // 2, y * TAILLE_CASE + TAILLE_CASE // 2)
                rayon = int(TAILLE_CASE * 0.4) # Le rond fait 40% de la case
                
                if entite == 'S': #Mouton
                    pygame.draw.circle(self.ecran, COULEUR_MOUTON, centre, rayon)
                
                elif entite == 'W': #Loup
                    pygame.draw.circle(self.ecran, COULEUR_LOUP, centre, rayon)

                # Optionnel : Petite bordure grise autour des cases pour bien voir la grille
                pygame.draw.rect(self.ecran, COULEUR_GRILLE, rect, 1)

        
        pygame.display.flip()

    def fermer(self):
        pygame.quit()



if __name__ == "__main__":
    GRID_SIZE = 30
    
    # Création de la structure vide
    grille = [[[0, "."] for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

    possibilites = ['W', 'S', '#', '.']
    
    # 1. Création de l'objet Afficheur (Instanciation)
    visu = Afficheur(grille)


    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            grille[y][x][0] = random.randint(0, 1)      # Herbe 0 ou 1
            grille[y][x][1] = random.choice(possibilites) # Animal
        
        
    visu.update(grille)
        
