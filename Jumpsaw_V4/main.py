import sys
import pygame

pygame.init()

from constantes import LARGEUR, HAUTEUR, FPS, FOND
from menu_V2 import Menu
from jeu import Jeu
from arene import Arene

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("A Slight Chance of Sawblades")
horloge = pygame.time.Clock()

ecrans = {
    "menu": Menu(money=150, score=1200, quota=2000),
    "jeu": Jeu(),
    "arene": Arene(money=150, score=1200, quota=2000),
}
actuel = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if actuel == "menu":
                pygame.quit()
                sys.exit()
            actuel = "menu"
            continue

        action = ecrans[actuel].gerer_evenement(event)
        if action == "quitter":
            pygame.quit()
            sys.exit()
        elif action in ecrans:
            if action == "jeu":
                ecrans["jeu"].reinitialiser()  # New Game = partie neuve
            actuel = action

    ecrans[actuel].mettre_a_jour()
    ecran.fill(FOND)
    ecrans[actuel].dessiner(ecran)
    pygame.display.flip()
    horloge.tick(FPS)
