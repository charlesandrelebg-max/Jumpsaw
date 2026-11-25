import random
import math
import pygame

pygame.init()

GRAVITE = 0.45
LARGEUR, HAUTEUR = 640, 360
FPS = 60


class Joueur:
    VITESSE = 4       
    FORCE_SAUT = 8    

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 30)
        self.couleur = (0, 0, 255)
        self.vy = 0
        self.au_sol = False

    def aller_gauche(self):
        self.rect.x -= self.VITESSE
        if self.rect.left < 0:
            self.rect.left = 0

    def aller_droite(self):
        self.rect.x += self.VITESSE
        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR

    def sauter(self):
        # On ne saute que si on touche le sol
        if self.au_sol:
            self.vy = -self.FORCE_SAUT   # négatif = vers le haut
            self.au_sol = False

    def deplacer(self, touches, plateformes):
        # --- axe X ---
        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.aller_gauche()
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.aller_droite()

        # (plus tard : collisions horizontales avec plateformes)

        # --- axe Y ---
        self.vy += GRAVITE                 # la gravité modifie la vitesse
        self.rect.y += round(self.vy)      # la vitesse déplace le joueur
        self.au_sol = False                # remis à True par une collision

        # sol provisoire (à remplacer par les plateformes)
        if self.rect.bottom > HAUTEUR:
            self.rect.bottom = HAUTEUR
            self.vy = 0
            self.au_sol = True

        # (plus tard : collisions verticales avec plateformes)

    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur, self.rect)


class Scie:
    def __init__(self, vitesse):
        self.rayon = 7
        self.x = random.randint(self.rayon, LARGEUR - self.rayon)
        self.y = self.rayon
        angle_depart = math.radians(7)
        signe = random.choice([-1, 1])
        self.vx = signe * vitesse * math.sin(angle_depart)
        self.vy = vitesse * math.cos(angle_depart)
        self.couleur = (255, 0, 0)
        self.angle = 0


class Caisse:
    def __init__(self, plateformes):
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.couleur = (255, 200, 0)
        self.repositionner(plateformes)


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("A Slight Chance of Sawblades")
        self.horloge = pygame.time.Clock()
        self.police = pygame.font.SysFont(None, 24)
        self.plateformes = []
        self.reinitialiser()

    def reinitialiser(self):
        self.joueur = Joueur(LARGEUR // 2, HAUTEUR - 30)
        self.scies = []
        self.caisse = Caisse(self.plateformes)
        self.score = 0
        self.temps = 0
        self.perdu = False

    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            if evenement.type == pygame.KEYDOWN:
                if evenement.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_z):
                    self.joueur.sauter()
        return True

    def mettre_a_jour(self):
        touches = pygame.key.get_pressed()
        self.joueur.deplacer(touches, self.plateformes)

    def dessiner(self):
        self.ecran.fill((30, 30, 40))
        self.joueur.dessiner(self.ecran)
        pygame.display.flip()

    def lancer(self):
        en_cours = True
        while en_cours:
            en_cours = self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            self.horloge.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    Jeu().lancer()