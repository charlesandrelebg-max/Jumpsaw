import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arene - Jumpsaw")

BACKGROUND = (30, 30, 60)
COLOR_TEXT = (185, 255, 255)

font_text = pygame.font.Font(None, 36)

class Arene:

  def __init__(self, money, score, quota):
    self.money = money
    self.score = score
    self.quota = quota
    self.objets = [Objet(400, 300), Objet(200, 400)]

  def generer_interface(self, surface, souris_pos):
    # Bandeau supérieur
    info_text = f"Argent : {self.money} $   |   Score : {self.score}   |   Quota : {self.quota}"
    surface.blit(font_text.render(info_text, True, COLOR_TEXT), (20, 20))
    
    # On parcourt une copie de la liste pour pouvoir supprimer des éléments en toute sécurité
        for obj in self.objets[:]:
            # Application de la physique (gravité optionnelle pour le sol)
            obj.vy += 0.3  # Gravité
            obj.deplacer()
            
            # --- 1. Murs (Côtés gauche et droit) ---
            if obj.x - obj.rayon < 0:
                obj.x = obj.rayon
                obj.vx = -obj.vx * 0.8  # Inversion de vitesse + perte d'énergie (rebond)
            elif obj.x + obj.rayon > WIDTH:
                obj.x = WIDTH - obj.rayon
                obj.vx = -obj.vx * 0.8

            # --- 2. Sol (Bas de la fenêtre) ---
            if obj.y + obj.rayon > HEIGHT:
                obj.y = HEIGHT - obj.rayon
                obj.vy = -obj.vy * 0.6  # Rebond sur le sol

            # --- 3. Plafond (Death Zone) ---
            # On fixe la limite de la death zone juste sous le bandeau textuel (par exemple y = 60)
            if obj.y - obj.rayon < 60:
                self.objets.remove(obj)
                self.score -= 50  # Petite pénalité de score par exemple
                print("Objet détruit par la death zone !")

            # Dessin de l'objet
                obj.dessiner(surface)
            else:
                obj.dessiner(surface)
                
    def augmenter_quota(self):
        if self.quota == 0:
            return self.quota = 200
        return self.quota = self.quota * 2
        
mon_arene = Arene(money=150, score=1200, quota=2000)
clock = pygame.time.Clock()
running = True

while running:
    souris_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

mon_menu = Menu(money=150, score=1200, quota=2000)
running = True

  screen.fill(BACKGROUND)
  mon_menu.generer_interface(screen, souris_pos)
  pygame.display.flip()

pygame.quit()
sys.exit()