import pygame
from constantes import (COULEUR_TEXTE, COULEUR_BOUTON,
                        COULEUR_BOUTON_SURVOL, LARGEUR)


class Menu:

    def __init__(self, money, score, quota):
        self.money = money
        self.score = score
        self.quota = quota

        # La police est créée ici (et pas en haut du fichier) car pygame.init()
        # est appelé dans main.py, après l'import de ce fichier.
        self.font_text = pygame.font.Font(None, 36)

        x = LARGEUR // 2 - 125  # boutons centrés quelle que soit la largeur
        self.btn_new_game = pygame.Rect(x, 180, 250, 50)
        self.btn_continue = pygame.Rect(x, 250, 250, 50)
        self.btn_shop = pygame.Rect(x, 320, 250, 50)
        self.btn_quit = pygame.Rect(x, 390, 250, 50)

    def dessiner_bouton(self, surface, rect, texte, souris_pos):
        couleur = COULEUR_BOUTON_SURVOL if rect.collidepoint(souris_pos) else COULEUR_BOUTON
        pygame.draw.rect(surface, couleur, rect, border_radius=8)
        pygame.draw.rect(surface, COULEUR_TEXTE, rect, 2, border_radius=8)

        txt_surf = self.font_text.render(texte, True, COULEUR_TEXTE)
        surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))

    def gerer_evenement(self, event):
        """Renvoie le nom de l'écran à afficher, "quitter", ou None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_new_game.collidepoint(event.pos):
                return "jeu"
            elif self.btn_continue.collidepoint(event.pos):
                return "arene"
            elif self.btn_shop.collidepoint(event.pos):
                print("Shop")  # pas encore codé
            elif self.btn_quit.collidepoint(event.pos):
                return "quitter"
        return None

    def mettre_a_jour(self):
        pass  # rien à animer dans le menu, mais main.py appelle cette méthode

    def dessiner(self, surface):
        souris_pos = pygame.mouse.get_pos()

        info_text = f"Argent : {self.money} $   |   Score : {self.score}   |   Quota : {self.quota}"
        surface.blit(self.font_text.render(info_text, True, COULEUR_TEXTE), (20, 20))

        self.dessiner_bouton(surface, self.btn_new_game, "New Game", souris_pos)
        self.dessiner_bouton(surface, self.btn_continue, "Continue", souris_pos)
        self.dessiner_bouton(surface, self.btn_shop, "Shop", souris_pos)
        self.dessiner_bouton(surface, self.btn_quit, "Quitter", souris_pos)
