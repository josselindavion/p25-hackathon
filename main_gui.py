import pygame
import sys
import math

## Importation des classes ##
import numpy as np
from entities import Wolf, Sheep, Grass
from grid import Grid
from constantes import(GRID_SIZE, INITIAL_SHEEP, INITIAL_WOLVES, MAX_TURNS, SHEEP_INITIAL_ENERGY, WOLF_INITIAL_ENERGY,
                      SHEEP_ENERGY_FROM_GRASS, WOLF_ENERGY_FROM_SHEEP, WOLF_ENERGY_LOSS_PER_TURN, SHEEP_ENERGY_LOSS_PER_TURN,
                      SHEEP_REPRODUCTION_THRESHOLD, WOLF_REPRODUCTION_THRESHOLD, REPRODUCTION_ENERGY_COST,
                      SHEEP_MAX_AGE, WOLF_MAX_AGE, GRASS_GROWTH_PROBABILITY, GRASS_REGROWTH_TIME,INITIAL_GRASS_COVERAGE)

## CONFIGURATION GRAPHIQUE ##
WINDOW_MAX_SIZE = 900 
CELL_SIZE = min(WINDOW_MAX_SIZE // GRID_SIZE[0], WINDOW_MAX_SIZE // GRID_SIZE[1])
WIDTH = GRID_SIZE[0] * CELL_SIZE
HEIGHT = GRID_SIZE[1] * CELL_SIZE
FPS = 5

## COULEURS ET FONCTIONS DE DESSIN ##
COLORS = {
    "BACKGROUND": (30, 30, 30),      ## Fond de la fenêtre (hors grille)
    "SOIL": (210, 180, 140),         ## Terre / Herbe morte (Tan)
    "GRASS": (106, 190, 48),         ## Herbe vivante (Vert doux)
    "GRASS_SHADOW": (90, 160, 40),   ## Ombre légère pour effet 3D
    "SHEEP_BODY": (245, 245, 245),   ## Blanc cassé
    "SHEEP_HEAD": (50, 50, 50),      ## Gris très foncé
    "WOLF_BODY": (44, 62, 80),       ## Bleu nuit/Gris foncé
    "WOLF_EYES": (231, 76, 60),      ## Rouge tomate
    "TEXT": (255, 255, 255),
    "HUD_BG": (0, 0, 0, 150)         ## Noir semi-transparent
}
## DESSIN DU LOUP ##
def draw_wolf(screen, x, y, size):
    ## Coordonnées du centre de la case##
    cx, cy = x + size // 2, y + size // 2
    radius = size // 2.5
    
    if size < 10:
        ## Si c'est tout petit, juste un point rouge ##
        pygame.draw.circle(screen, COLORS["WOLF_EYES"], (cx, cy), size//2)
        return

    ## Corps (Triangle) ##
    point1 = (cx, cy - radius)          # Haut
    point2 = (cx - radius, cy + radius) # Bas Gauche
    point3 = (cx + radius, cy + radius) # Bas Droite
    pygame.draw.polygon(screen, COLORS["WOLF_BODY"], [point1, point2, point3])
    
    ## Yeux (si l'écran est assez grand) ##
    if size > 20:
        eye_y = cy - radius // 4
        pygame.draw.circle(screen, COLORS["WOLF_EYES"], (cx - radius//3, eye_y), 2)
        pygame.draw.circle(screen, COLORS["WOLF_EYES"], (cx + radius//3, eye_y), 2)


## DESSIN DU MOUTON ##
def draw_sheep(screen, x, y, size):
    cx, cy = x + size // 2, y + size // 2
    radius = size // 3
    
    if size < 10:
        ## Si c'est tout petit, juste un point blanc ##
        pygame.draw.circle(screen, COLORS["SHEEP_BODY"], (cx, cy), size//2)
        return

    ## Corps (Cercle principal) ##
    pygame.draw.circle(screen, COLORS["SHEEP_BODY"], (cx, cy), radius)
    
    ## Tête (Petit cercle noir décalé) ##
    if size > 15:
        head_radius = radius // 1.5
        ## La tête est un peu en bas à droite ou au centre ##
        pygame.draw.circle(screen, COLORS["SHEEP_HEAD"], (cx, cy - radius//2), head_radius)

## DESSIN DE LA GRILLE ##
## On fait une grille pretty grr"
def draw_grid_pretty(screen, grid):
    
    ## La terre en fond ##
    screen.fill(COLORS["SOIL"])

    ## DESSIN DES CASES GRASS VIVANTES ##
    for grass in grid.list_grass:
        if grass.alive:
            x_px = grass.position[0] * CELL_SIZE
            y_px = grass.position[1] * CELL_SIZE
            
            ## EFFET TUILE 3D STYLE DE FOU ##
            margin = 1 if CELL_SIZE > 10 else 0
            rect = pygame.Rect(x_px + margin, y_px + margin, CELL_SIZE - margin*2, CELL_SIZE - margin*2)
            pygame.draw.rect(screen, COLORS["GRASS"], rect)
            
            ## EFFET DE VOLUME ##
            if CELL_SIZE > 15:
                shadow_h = max(2, CELL_SIZE // 10)
                shadow_rect = pygame.Rect(x_px + margin, y_px + CELL_SIZE - margin - shadow_h, CELL_SIZE - margin*2, shadow_h)
                pygame.draw.rect(screen, COLORS["GRASS_SHADOW"], shadow_rect)

    ## DESSIN DES MOUTONS ET LOUPS ##
    for sheep in grid.list_sheep:
        if sheep.alive:
            draw_sheep(screen, sheep.position[0] * CELL_SIZE, sheep.position[1] * CELL_SIZE, CELL_SIZE)

    ## LES LOUPS ##
    for wolf in grid.list_wolf:
        if wolf.alive:
            draw_wolf(screen, wolf.position[0] * CELL_SIZE, wolf.position[1] * CELL_SIZE, CELL_SIZE)

## AFFICHAGE DES STATS ##
def draw_hud(screen, tour, n_sheep, n_wolves):
    font = pygame.font.SysFont("Verdana", 20, bold=True)
    
    text_t = font.render(f"TOUR {tour}", True, COLORS["TEXT"])
    text_s = font.render(f"Moutons: {n_sheep}", True, COLORS["SHEEP_BODY"])
    text_w = font.render(f"Loups: {n_wolves}", True, COLORS["WOLF_EYES"])
    
    ## Dimensions du panneau ##
    padding = 15
    total_width = text_t.get_width() + text_s.get_width() + text_w.get_width() + padding * 4
    panel_height = 40
    
    ## Création d'une surface transparente pour le fond ##
    hud_surface = pygame.Surface((total_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(hud_surface, COLORS["HUD_BG"], hud_surface.get_rect(), border_radius=10)
    
    ## Positionnement en haut au centre ##
    screen_x = (WIDTH - total_width) // 2
    screen.blit(hud_surface, (screen_x, 10))
    
    ## LE TEXTE ##
    current_x = screen_x + padding
    screen.blit(text_t, (current_x, 18))
    current_x += text_t.get_width() + padding
    screen.blit(text_s, (current_x, 18))
    current_x += text_s.get_width() + padding
    screen.blit(text_w, (current_x, 18))

## AFFICHAGE PRINCIPAL - NOUVELLE FTC MAIN ##
def main_gui():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Écosystème: Loups & Moutons")
    clock = pygame.time.Clock()
    
    ## On reprend les trucs de main ##
    grid = Grid(GRID_SIZE[0], GRID_SIZE[1])
    grid.initialisation(INITIAL_SHEEP, INITIAL_WOLVES)

    running = True
    paused = True
    tour_count = 0
    simulation_active = True

    #€# Texte PAUSE gros ##
    big_font = pygame.font.SysFont("Verdana", 60, bold=True)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused and simulation_active:
            simulation_continue = grid.evolve()
            tour_count += 1
            if not simulation_continue:
                simulation_active = False
                print("Fin de simulation.")

        ## DESSIN GRAPHIQUE ##
        draw_grid_pretty(screen, grid)
        draw_hud(screen, tour_count, len(grid.list_sheep), len(grid.list_wolf))

        if paused:
            ## Ecran assombri en mode pause ##
            dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 100))
            screen.blit(dark_overlay, (0,0))
            
            ## Texte de pause centré ##
            pause_text = big_font.render("PAUSE", True, COLORS["TEXT"])
            text_rect = pause_text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(pause_text, text_rect)
            
            sub_text = pygame.font.SysFont("Verdana", 20).render("Appuyez sur ESPACE", True, COLORS["TEXT"])
            sub_rect = sub_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
            screen.blit(sub_text, sub_rect)

        pygame.display.flip()
        
        if paused:
            clock.tick(30)
        else:
            clock.tick(FPS)

    pygame.quit()
    sys.exit()
