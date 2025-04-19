import pygame


class ImageButton:
    def __init__(self, x, y, image_path, scale=1.0):
        self.image = pygame.image.load(image_path).convert_alpha() # Charge l'image du bouton avec transparence
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * scale), int(self.image.get_height() * scale)))# Mise à l'échelle de l'image
        self.rect = self.image.get_rect(topleft=(x, y)) # Détermine la zone de collision du bouton

    def draw(self, screen): # Affiche le bouton à sa position
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos): # Vérifie si la position du clic est à l'intérieur du bouton
        return self.rect.collidepoint(pos)

