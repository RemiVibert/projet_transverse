import pygame
import random


class Collectible:
    def __init__(self, pos:pygame.Vector2, game):
        self.pos = pos 
        self.image = pygame.image.load('assets/sprites/collectibles/collectible.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)  # Crée un rectangle de collision
        self.original_image = self.image  # Garde l’image de base pour les rescalings
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.randint(1, 4)
        self.game = game

    def update(self):
        self.rotation += self.rotation_speed
        self.rotation %= 360

    def collect(self):
        """Retire l'objet de la liste des collectibles"""
        self.game.collectibles.remove(self)
        self.game.collectibles.remove(self)
        self.game.collected_collectibles += 1
        # Pas besoin de détruire l'objet, le retirer de la liste suffit à ne plus l'afficher, et comme on en a pas 500, ça prend pas de place en mémoire
        
        



    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom) # Applique un zoom à l'image de la planète
        scaled_image = pygame.transform.rotate(scaled_image, self.rotation)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Calcule le rectangle de dessin pour que la planète soit centrée correctement
        

        
        screen.blit(scaled_image, new_rect) # Affiche l’image de la planète à l’écran

        # === DEBUG == #
        # Affiche le rect du collectible avec un rectangle vert transparent
        #rect_surface = pygame.Surface((new_rect.width, new_rect.height), pygame.SRCALPHA)
        #rect_surface.fill((0, 255, 0, 50))  # Vert transparent # mettre le "50" à 0 pour rendre invisible
        #screen.blit(rect_surface, new_rect.topleft)
