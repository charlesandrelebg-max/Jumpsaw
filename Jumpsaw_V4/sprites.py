import os
import pygame

# Les images sont cherchées dans le même dossier que ce fichier.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def charger(nom):
    """Charge une image une seule fois (ensuite on la réutilise).
    À appeler APRÈS pygame.display.set_mode (nécessaire pour convert_alpha).
    Si le fichier est introuvable, on affiche un message et on utilise un
    carré rose à la place : le jeu ne plante pas."""
    if nom not in _cache:
        chemin = os.path.join(DOSSIER, nom)
        try:
            _cache[nom] = pygame.image.load(chemin).convert_alpha()
        except (FileNotFoundError, pygame.error):
            print(f"[ATTENTION] Image introuvable : {chemin}")
            surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            surface.fill((255, 0, 255))
            _cache[nom] = surface
    return _cache[nom]
