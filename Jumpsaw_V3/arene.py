import random
import pygame
from constantes import LARGEUR, HAUTEUR, COULEUR_TEXTE

ZONE_MORTE_Y = 60  # sous le bandeau de texte : au-dessus de cette ligne, on perd l'objet


class Objet:

    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.rayon = 15
        self.couleur = (255, 180, 0)

    def deplacer(self):
        self.x += self.vx
        self.y += self.vy

    def dessiner(self, surface):
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), self.rayon)


class Arene:

    def __init__(self, money, score, quota):
        self.money = money
        self.score = score
        self.quota = quota
        self.font_text = pygame.font.Font(None, 36)
        self.objets = [Objet(400, 300, vx=2), Objet(200, 400, vx=-2)]

    def gerer_evenement(self, event):
        # Clic gauche : lance un objet vers le haut pour tester la zone morte
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] > ZONE_MORTE_Y + 20:
                self.objets.append(Objet(event.pos[0], event.pos[1],
                                         vx=random.uniform(-3, 3),
                                         vy=random.uniform(-14, -6)))
        return None

    def mettre_a_jour(self):
        # On parcourt une COPIE de la liste ([:]) pour pouvoir
        # supprimer des éléments pendant la boucle sans bug.
        for obj in self.objets[:]:
            obj.vy += 0.3  # gravité
            obj.deplacer()

            # Murs gauche / droite : rebond avec perte d'énergie
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

            # Plafond = zone morte
            if obj.y - obj.rayon < ZONE_MORTE_Y:
                self.objets.remove(obj)
                self.score -= 50
                print("Objet détruit par la death zone !")

    def augmenter_quota(self):
        if self.quota == 0:
            self.quota = 200
        else:
            self.quota = self.quota * 2
        return self.quota

    def dessiner(self, surface):
        info_text = f"Argent : {self.money} $   |   Score : {self.score}   |   Quota : {self.quota}"
        surface.blit(self.font_text.render(info_text, True, COULEUR_TEXTE), (20, 20))

        # Ligne rouge de la zone morte
        pygame.draw.line(surface, (200, 40, 40), (0, ZONE_MORTE_Y), (LARGEUR, ZONE_MORTE_Y), 2)

        for obj in self.objets:
            obj.dessiner(surface)
