import pygame
import math

pygame.init()
Gravité = 0,45
LARGEUR, HAUTEUR = 640, 360
FPS = 60

class Joueur:

    def__init__(self, x, y):
        self.rect = pygame.rect(x, y, 20, 100)
        self.couleur = (0,0,255)
        self.vy = 0
        self.au_sol = False

class Scie:
    def__init__(self, vitesse):
        self.rayon = 7
        self.x = random.randint(self.rayon, LARGEUR-self.rayon)
        self.y = random.randint(self.rayon, HAUTEUR-self.rayon)
        self.vx = vitesse*sin(7)
        self.vy = vitesse*cos(7)
        self.couleur = (255, 0, 0)


