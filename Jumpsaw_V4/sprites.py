import os
import pygame

# Les images sont cherchées dans le même dossier que ce fichier.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
_cache = {}


def charger(nom):
    """Charge une image une seule fois (ensuite on la réutilise).
    À appeler APRÈS pygame.display.set_mode (nécessaire pour convert_alpha)."""
    if nom not in _cache:
        chemin = os.path.join(DOSSIER, nom)
        _cache[nom] = pygame.image.load(chemin).convert_alpha()
    return _cache[nom]
