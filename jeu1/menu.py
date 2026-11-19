from turtle import *
from pygame import *
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600

# Création de la fenêtre
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Erreur lors de la création de la fenêtre : {e}")
    pygame.quit()
    sys.exit()

pygame.display.set_caption("Fenêtre Pygame")

BACKGROUND_COLOR = ("blue")

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Touche Échap pour quitter
                running = False

    screen.fill(BACKGROUND_COLOR)

    pygame.display.flip()

pygame.quit()
sys.exit()

class Menu:
    def __init__(self, money, score, quota):
        self.money = money
        self.score = score
        self.quota = quota
    def génerer_interface(self):
