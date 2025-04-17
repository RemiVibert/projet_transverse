import pygame


class ImageButton:
    def __init__(self, x, y, image_path, scale=1.0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

