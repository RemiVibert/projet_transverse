import pygame


class ImageButton:
    def __init__(self, x, y, image_path, hover_image_path = None, width=None, height=None):

        default_raw = pygame.image.load(image_path).convert_alpha() # Charge l'image de base du bouton avec transparence
        target_size = (  # Détermine la taille finale du bouton
            width if width else default_raw.get_width(),
            height if height else default_raw.get_height()
        )
        self.default_image = pygame.transform.scale(default_raw, target_size)  # Redimensionne l'image par défaut à la taille voulue

        if hover_image_path:   # Si une image de survol est fournie, on la charge et on la redimensionne
            hover_raw = pygame.image.load(hover_image_path).convert_alpha()
            self.hover_image = pygame.transform.scale(hover_raw, target_size)
        else:
            self.hover_image = self.default_image  # Sinon, le bouton reste identique au survol

        self.image = self.default_image
        self.rect = self.image.get_rect(topleft=(x, y)) # Détermine la zone de collision du bouton

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos): # Si la souris est sur le bouton affiche l'image de survol
            self.image = self.hover_image
        else:
            self.image = self.default_image

    def draw(self, screen): # Affiche le bouton à sa position
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos): # Vérifie si la position du clic est à l'intérieur du bouton
        return self.rect.collidepoint(pos)

