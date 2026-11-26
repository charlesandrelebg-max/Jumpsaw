import random
import math
import pygame
from constantes import LARGEUR, HAUTEUR, COULEUR_TEXTE
from sprites import charger

GRAVITE = 0.45


class Joueur:
    VITESSE = 4
    FORCE_SAUT = 8

    def __init__(self, x, y):
        """(x, y) = milieu du bas du personnage (ses pieds)."""
        self.img_droite = charger("perso_course_D.png")
        self.img_gauche = charger("perso_course_G.png")
        self.img_immobile = charger("perso_immobile.png")
        self.img_saut = charger("perso_saut.png")
        self.img_mort = charger("perso_mort.png")

        self.image = self.img_immobile
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # hitbox pixel par pixel
        self.vy = 0
        self.au_sol = False
        self.direction = 0  # -1 gauche, 0 immobile, 1 droite
        self.mort = False

    @property
    def hitbox(self):
        # Rectangle un peu plus petit que le sprite (pour ramasser les caisses)
        return self.rect.inflate(-8, -4)

    def aller_gauche(self):
        self.rect.x -= self.VITESSE
        if self.rect.left < 0:
            self.rect.left = 0

    def aller_droite(self):
        self.rect.x += self.VITESSE
        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR

    def sauter(self):
        if self.au_sol and not self.mort:
            self.vy = -self.FORCE_SAUT
            self.au_sol = False

    def choisir_image(self):
        if self.mort:
            self.image = self.img_mort
        elif not self.au_sol:
            self.image = self.img_saut
        elif self.direction == 1:
            self.image = self.img_droite
        elif self.direction == -1:
            self.image = self.img_gauche
        else:
            self.image = self.img_immobile

        # Les images n'ont pas toutes la même taille : on garde les pieds au même endroit
        pieds = self.rect.midbottom
        self.rect = self.image.get_rect(midbottom=pieds)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR:
            self.rect.right = LARGEUR
        self.mask = pygame.mask.from_surface(self.image)

    def deplacer(self, touches, plateformes):
        self.direction = 0
        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.aller_gauche()
            self.direction = -1
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.aller_droite()
            self.direction = 1

        self.vy += GRAVITE
        self.rect.y += round(self.vy)
        self.au_sol = False

        # sol provisoire (à remplacer par les plateformes)
        # ">=" et pas ">" : sinon le joueur est "au sol" une frame sur deux
        # et le saut ne répond qu'une fois sur deux.
        if self.rect.bottom >= HAUTEUR:
            self.rect.bottom = HAUTEUR
            self.vy = 0
            self.au_sol = True

        self.choisir_image()

    def dessiner(self, surface):
        surface.blit(self.image, self.rect)


class Scie:
    def __init__(self, vitesse):
        self.image = charger("pique.png")
        # Si tu veux la pointe vers le bas, décommente :
        # self.image = pygame.transform.flip(self.image, False, True)
        self.mask = pygame.mask.from_surface(self.image)
        self.rayon = self.image.get_width() // 2

        self.x = random.randint(self.rayon, LARGEUR - self.rayon)
        self.y = self.rayon
        angle_depart = math.radians(7)
        signe = random.choice([-1, 1])
        self.vx = signe * vitesse * math.sin(angle_depart)
        self.vy = vitesse * math.cos(angle_depart)
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))

    def deplacer(self):
        self.x += self.vx
        self.y += self.vy
        # rebond sur les murs latéraux
        if self.x - self.rayon < 0:
            self.x = self.rayon
            self.vx = -self.vx
        elif self.x + self.rayon > LARGEUR:
            self.x = LARGEUR - self.rayon
            self.vx = -self.vx
        self.rect.center = (round(self.x), round(self.y))

    def est_sortie(self):
        return self.rect.top > HAUTEUR

    def touche(self, joueur):
        # 1) test rapide avec les rectangles
        if not self.rect.colliderect(joueur.rect):
            return False
        # 2) test précis : les pixels visibles des deux sprites se chevauchent ?
        decalage = (joueur.rect.x - self.rect.x, joueur.rect.y - self.rect.y)
        return self.mask.overlap(joueur.mask, decalage) is not None

    def dessiner(self, surface):
        surface.blit(self.image, self.rect)


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
        self.joueur = Joueur(LARGEUR // 2, HAUTEUR)
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
            if scie.touche(self.joueur):
                self.perdu = True
                self.joueur.mort = True
                self.joueur.choisir_image()
            elif scie.est_sortie():
                self.scies.remove(scie)

        if self.joueur.hitbox.colliderect(self.caisse.rect):
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
