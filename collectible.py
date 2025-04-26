import pygame
import random


class Collectible:
    def __init__(self, pos:pygame.Vector2):
        self.pos = pos 
        self.image = pygame.image.load('assets/sprites/collectibles/collectible.png').convert_alpha()
        self.original_image = self.image  # Garde l’image de base pour les rescalings
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.randint(-5, 5)

    def update(self):
        self.rotation += self.rotation_speed
        self.rotation %= 360

    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom) # Applique un zoom à l'image de la planète
        scaled_image = pygame.transform.rotate(scaled_image, self.rotation)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Calcule le rectangle de dessin pour que la planète soit centrée correctement
        screen.blit(scaled_image, new_rect) # Affiche l’image de la planète à l’écran
