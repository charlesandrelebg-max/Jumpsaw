import random
import pygame
from constantes import LARGEUR, HAUTEUR, COULEUR_TEXTE

LIMITE_DEATH_ZONE = 60  # juste sous le bandeau de texte


class Objet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.choice([-3, 3])
        self.vy = 0
        self.rayon = 15
        self.couleur = (255, 200, 0)

    def deplacer(self):
        self.x += self.vx
        self.y += self.vy

    def dessiner(self, surface):
        pygame.draw.circle(surface, self.couleur, (round(self.x), round(self.y)), self.rayon)


class Arene:

    def __init__(self, money, score, quota):
        self.money = money
        self.score = score
        self.quota = quota
        self.police = pygame.font.Font(None, 36)
        self.objets = [Objet(400, 300), Objet(200, 400)]

    def gerer_evenement(self, event):
        return None

    def mettre_a_jour(self):
        # On parcourt une copie de la liste pour pouvoir supprimer en toute sécurité
        for obj in self.objets[:]:
            obj.vy += 0.3  # gravité
            obj.deplacer()

            # Murs gauche et droit
            if obj.x - obj.rayon < 0:
                obj.x = obj.rayon
                obj.vx = -obj.vx * 0.8
            elif obj.x + obj.rayon > LARGEUR:
                obj.x = LARGEUR - obj.rayon
                obj.vx = -obj.vx * 0.8

            # Sol
            if obj.y + obj.rayon > HAUTEUR:
                obj.y = HAUTEUR - obj.rayon
                obj.vy = -obj.vy * 0.6
                if abs(obj.vy) < 1:  # évite de trembler sur place
                    obj.vy = 0

            # Plafond (death zone)
            if obj.y - obj.rayon < LIMITE_DEATH_ZONE:
                self.objets.remove(obj)
                self.score -= 50
                print("Objet détruit par la death zone !")

    def augmenter_quota(self):
        if self.quota == 0:
            self.quota = 200
        else:
            self.quota = self.quota * 2

    def dessiner(self, surface):
        info = f"Argent : {self.money} $   |   Score : {self.score}   |   Quota : {self.quota}"
        surface.blit(self.police.render(info, True, COULEUR_TEXTE), (20, 20))
        pygame.draw.line(surface, (200, 50, 50), (0, LIMITE_DEATH_ZONE), (LARGEUR, LIMITE_DEATH_ZONE), 2)
        for obj in self.objets:
            obj.dessiner(surface)
