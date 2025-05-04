import pygame

class Base:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)