import random
import math
import pygame
from constantes import LARGEUR, HAUTEUR, COULEUR_TEXTE

GRAVITE = 0.45


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
        if self.au_sol:
            self.vy = -self.FORCE_SAUT
            self.au_sol = False

    def deplacer(self, touches, plateformes):
        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.aller_gauche()
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.aller_droite()

        self.vy += GRAVITE
        self.rect.y += round(self.vy)
        self.au_sol = False

        # sol provisoire (à remplacer par les plateformes)
        if self.rect.bottom > HAUTEUR:
            self.rect.bottom = HAUTEUR
            self.vy = 0
            self.au_sol = True

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

    def deplacer(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += 15
        # rebond sur les murs latéraux
        if self.x - self.rayon < 0:
            self.x = self.rayon
            self.vx = -self.vx
        elif self.x + self.rayon > LARGEUR:
            self.x = LARGEUR - self.rayon
            self.vx = -self.vx

    def est_sortie(self):
        return self.y - self.rayon > HAUTEUR

    def touche(self, rect):
        # point du rectangle le plus proche du centre de la scie
        px = max(rect.left, min(self.x, rect.right))
        py = max(rect.top, min(self.y, rect.bottom))
        return (self.x - px) ** 2 + (self.y - py) ** 2 < self.rayon ** 2

    def dessiner(self, surface):
        centre = (int(self.x), int(self.y))
        pygame.draw.circle(surface, self.couleur, centre, self.rayon)
        # un trait qui tourne pour donner l'impression que la scie tourne
        a = math.radians(self.angle)
        fin = (centre[0] + math.cos(a) * self.rayon, centre[1] + math.sin(a) * self.rayon)
        pygame.draw.line(surface, (255, 255, 255), centre, fin, 2)


class Caisse:
    def __init__(self, plateformes):
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.couleur = (255, 200, 0)
        self.repositionner(plateformes)

    def repositionner(self, plateformes):
        # Sans plateformes : position aléatoire, à portée de saut du joueur
        self.rect.x = random.randint(0, LARGEUR - self.rect.width)
        self.rect.bottom = HAUTEUR - random.randint(0, 50)

    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur, self.rect)


class Jeu:
    def __init__(self):
        self.police = pygame.font.Font(None, 28)
        self.plateformes = []
        self.reinitialiser()

    def reinitialiser(self):
        self.joueur = Joueur(LARGEUR // 2, HAUTEUR - 30)
        self.scies = []
        self.caisse = Caisse(self.plateformes)
        self.score = 0
        self.temps = 0
        self.perdu = False

    def gerer_evenement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_z):
                self.joueur.sauter()
            if event.key == pygame.K_r and self.perdu:
                self.reinitialiser()
        return None

    def mettre_a_jour(self):
        if self.perdu:
            return
        self.temps += 1
        touches = pygame.key.get_pressed()
        self.joueur.deplacer(touches, self.plateformes)

        # une nouvelle scie toutes les 1,5 s environ
        if self.temps % 90 == 0:
            self.scies.append(Scie(3))

        for scie in self.scies[:]:
            scie.deplacer()
            if scie.touche(self.joueur.rect):
                self.perdu = True
            elif scie.est_sortie():
                self.scies.remove(scie)

        if self.joueur.rect.colliderect(self.caisse.rect):
            self.score += 1
            self.caisse.repositionner(self.plateformes)

    def dessiner(self, surface):
        self.caisse.dessiner(surface)
        self.joueur.dessiner(surface)
        for scie in self.scies:
            scie.dessiner(surface)

        surface.blit(self.police.render(f"Caisses : {self.score}", True, COULEUR_TEXTE), (20, 20))
        if self.perdu:
            msg = self.police.render("Perdu ! R pour rejouer, Echap pour le menu", True, COULEUR_TEXTE)
            surface.blit(msg, msg.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
