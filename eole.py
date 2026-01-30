import pygame
import sys

# --- PARAMÈTRES D'AFFICHAGE ---
TAILLE_CASE = 20          # 30 cases * 20 pixels = fenêtre de 600x600 pixels
COULEUR_TERRE = (139, 69, 19)    # Marron (Sol vide)
COULEUR_HERBE = (34, 139, 34)    # Vert (Herbe)
COULEUR_MOUTON = (255, 255, 255) # Blanc (Mouton)
COULEUR_LOUP = (220, 20, 60)     # Rouge (Loup)
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