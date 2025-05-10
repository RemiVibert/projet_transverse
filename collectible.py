import pygame
import random
from player import Player


class Collectible:
    def __init__(self, pos:pygame.Vector2, game):
        """
            Initialise un collectible (=astronaute).

            Args:
            pos (pygame.Vector2): Position du collectible dans le monde.
            game: Référence au jeu pour accéder aux éléments globaux.
        """
        self.pos = pos
        self.image = pygame.image.load('assets/sprites/collectibles/collectible.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)  # Crée un rectangle de collision
        self.original_image = self.image  # Garde l’image de base pour les rescalings
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.randint(1, 4) # Vitesse de rotation aléatoire
        self.game = game
        self.collected = False # Indique si l'objet a été collecté

    def update(self):
        # Met à jour la rotation du collectible
        self.rotation += self.rotation_speed
        self.rotation %= 360

    def collect(self):
        #Retire l'objet de la liste des collectibles
        if not self.collected:
            self.collected = True
            if self in self.game.collectibles:
                self.game.collectibles.remove(self)
            self.game.player.collected_collectibles += 1



    def draw(self, screen, camera):
        # Applique le zoom et la rotation, puis affiche l'image à l'écran
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom)
        scaled_image = pygame.transform.rotate(scaled_image, self.rotation)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Calcule le rectangle de dessin pour que la planète soit centrée correctement
        screen.blit(scaled_image, new_rect) # Affiche le collectible à sa position

