import pygame
import random

class Etoiles(pygame.sprite.Sprite):
    def __init__(self, nb_etoiles, max_x, max_y, min_x, min_y):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/decor/star.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.etoiles = []
        for i in range(nb_etoiles):
            pos = pygame.Vector2(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
            profondeur = random.uniform(0.10, 0.50)
            self.etoiles.append({"pos": pos, "profondeur": profondeur})
        
    
    def draw(self, screen, camera):
        for etoile in self.etoiles:
            parralax_offset = camera.offset * etoile["profondeur"]
            screen_pos = (etoile["pos"] - parralax_offset) * camera.zoom
            size = camera.zoom * etoile["profondeur"]
            scaled_image = pygame.transform.rotozoom(self.image, 0, size)
            new_rect = scaled_image.get_rect(center=(screen_pos.x, screen_pos.y))
            screen.blit(scaled_image, new_rect)




