import sys
import pygame
import subprocess
from constantes import LARGEUR, HAUTEUR, COULEUR_TEXTE

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal - NSI")

BACKGROUND_COLOR = (30, 30, 60)
COLOR_TEXT = (185, 255, 255)
COLOR_BTN = (24, 12, 91)
COLOR_BTN_HOVER = (50, 30, 150)

font_text = pygame.font.Font(None, 36)


class Menu:

  def __init__(self, money, score, quota):
    self.money = money
    self.score = score
    self.quota = quota

    self.btn_new_game = pygame.Rect(275, 180, 250, 50)
    self.btn_continue = pygame.Rect(275, 250, 250, 50)
    self.btn_shop = pygame.Rect(275, 320, 250, 50)
    self.btn_quit = pygame.Rect(275, 390, 250, 50)

  def dessiner_bouton(self, surface, rect, texte, souris_pos):
    couleur = COLOR_BTN_HOVER if rect.collidepoint(souris_pos) else COLOR_BTN
    pygame.draw.rect(surface, couleur, rect, border_radius=8)
    pygame.draw.rect(surface, COLOR_TEXT, rect, 2, border_radius=8)

    txt_surf = font_text.render(texte, True, COLOR_TEXT)
    txt_rect = txt_surf.get_rect(center=rect.center)
    surface.blit(txt_surf, txt_rect)

  def generer_interface(self, surface, souris_pos):
    # Bandeau supérieur
    info_text = f"Argent : {self.money} $   |   Score : {self.score}   |   Quota : {self.quota}"
    surface.blit(font_text.render(info_text, True, COLOR_TEXT), (20, 20))

    # Boutons
    self.dessiner_bouton(surface, self.btn_new_game, "New Game", souris_pos)
    self.dessiner_bouton(surface, self.btn_continue, "Continue", souris_pos)
    self.dessiner_bouton(surface, self.btn_shop, "Shop", souris_pos)
    self.dessiner_bouton(surface, self.btn_quit, "Quitter", souris_pos)

  def gerer_clics(self, pos):
    if self.btn_new_game.collidepoint(pos):
      quota = 100
      subprocess.run(["arene.py"])
    elif self.btn_continue.collidepoint(pos):
      subprocess.run(["arene.py"])
    elif self.btn_shop.collidepoint(pos):
      print("Shop")
    elif self.btn_quit.collidepoint(pos):
      return False  # Signale l'arrêt de la boucle principale
    return True


mon_menu = Menu(money=150, score=1200, quota=2000)
running = True

while running:
  souris_pos = pygame.mouse.get_pos()

  for event in pygame.event.get():
    if event.type == pygame.QUIT or (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ):
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      running = mon_menu.gerer_clics(event.pos)

  screen.fill(BACKGROUND_COLOR)
  mon_menu.generer_interface(screen, souris_pos)
  pygame.display.flip()

pygame.quit()
sys.exit()