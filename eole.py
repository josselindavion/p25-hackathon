import pygame
import sys
import random

from nico import Wolf

#Paramètres d'affichage
TAILLE_CASE = 20          
COULEUR_TERRE = (139, 69, 19)    # Marron (Sol vide)
COULEUR_HERBE = (34, 139, 34)    # Vert (Herbe)
COULEUR_MOUTON = (255, 255, 255) # Blanc (Mouton)
COULEUR_LOUP = (0, 0, 0)     # Noir (Loup)
COULEUR_GRILLE = (50, 50, 50) 
COULEUR_LOUP_YEUX = (100, 100, 100)   # Gris foncé (Lignes de séparation)

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
                
                # --- DESSIN DU SOL (Inchangé) ---
                rect = (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                if herbe_presente == 1 or entite == '#':
                    pygame.draw.rect(self.ecran, COULEUR_HERBE, rect)
                else:
                    pygame.draw.rect(self.ecran, COULEUR_TERRE, rect)
                
                # --- DESSIN DES ENTITÉS ---
                # Coordonnées du centre de la case actuelle
                centre_x = x * TAILLE_CASE + TAILLE_CASE // 2
                centre_y = y * TAILLE_CASE + TAILLE_CASE // 2
                centre = (centre_x, centre_y)
                
                if entite == 'S': # Mouton (Simple rond blanc avec un contour gris)
                    rayon = int(TAILLE_CASE * 0.35)
                    pygame.draw.circle(self.ecran, COULEUR_MOUTON, centre, rayon)
                    # Petit contour pour le style
                    pygame.draw.circle(self.ecran, (200,200,200), centre, rayon, 1) 
                
                # --- LE NOUVEAU DESSIN DU LOUP EST ICI ---
                elif entite == 'W': # Loup stylisé
                    rayon_tethe = int(TAILLE_CASE * 0.35)
                    
                    # 1. Les Oreilles (Triangles)
                    # On les dessine EN PREMIER pour qu'elles soient "derrière" la tête
                    offset_oreille_x = int(TAILLE_CASE * 0.25)
                    offset_oreille_y = int(TAILLE_CASE * 0.3)
                    pointe_oreille_y = int(TAILLE_CASE * 0.5) # Hauteur de la pointe

                    # Oreille gauche (3 points du triangle)
                    p1_g = (centre_x - offset_oreille_x, centre_y - offset_oreille_y) # base gauche
                    p2_g = (centre_x - offset_oreille_x + 2, centre_y - pointe_oreille_y) # pointe haute
                    p3_g = (centre_x, centre_y - offset_oreille_y - 2) # base droite
                    pygame.draw.polygon(self.ecran, COULEUR_LOUP, [p1_g, p2_g, p3_g])
                    
                    # Oreille droite (Miroir de l'oreille gauche sur l'axe X)
                    p1_d = (centre_x + offset_oreille_x, centre_y - offset_oreille_y)
                    p2_d = (centre_x + offset_oreille_x - 2, centre_y - pointe_oreille_y)
                    p3_d = (centre_x, centre_y - offset_oreille_y - 2)
                    pygame.draw.polygon(self.ecran, COULEUR_LOUP, [p1_d, p2_d, p3_d])

                    # 2. La Tête (Rond par-dessus les bases des oreilles)
                    pygame.draw.circle(self.ecran, COULEUR_LOUP, centre, rayon_tethe)
                    
                    # 3. Les Yeux (Petits ronds jaunes)
                    offset_yeux_x = int(TAILLE_CASE * 0.15)
                    offset_yeux_y = int(TAILLE_CASE * 0.05)
                    rayon_yeux = int(TAILLE_CASE * 0.08)
                    
                    # Oeil gauche
                    pygame.draw.circle(self.ecran, COULEUR_LOUP_YEUX, (centre_x - offset_yeux_x, centre_y - offset_yeux_y), rayon_yeux)
                    # Oeil droit
                    pygame.draw.circle(self.ecran, COULEUR_LOUP_YEUX, (centre_x + offset_yeux_x, centre_y - offset_yeux_y), rayon_yeux)

                # Optionnel : Petite bordure grise autour des cases pour bien voir la grille
                pygame.draw.rect(self.ecran, COULEUR_GRILLE, rect, 1)
        
        pygame.display.flip()

    def fermer(self):
        pygame.quit()




GRID_SIZE = 10
    
# Création de la structure vide
grille = [[[0, "."] for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

possibilites = ['W', 'S', '#', '.']
    
    # 1. Création de l'objet Afficheur (Instanciation)
visu = Afficheur(grille)


for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        grille[y][x][0] = random.randint(0, 1)      # Herbe 0 ou 1
        grille[y][x][1] = random.choice(possibilites) # Animal
        
while True:    
    visu.update(grille)
        