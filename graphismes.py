import pygame
import random

class Etoiles(pygame.sprite.Sprite):
    def __init__(self, nb_etoiles, max_x, max_y, min_x, min_y):
        """
            Initialise les étoiles dans le fond du jeu.

            Args:
            nb_etoiles (int) : nombre d'étoiles à faire apparaitre
            max_x (int) : position en minimum en x des étoiles
            max_y (int) : position en minimum en y des étoiles
            min_x (int) : position au maximum en x des étoiles
            min_y (int) : position au maximum en y des étoiles
        """
        super().__init__()
        self.image = pygame.image.load("assets/sprites/decor/star.png") # Charge l'image des étoiles
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.etoiles = []  # Initialise une liste vide qui contiendra la postion et profondeur de chaque étoile

        for i in range(nb_etoiles):
            pos = pygame.Vector2(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) # Génère une position aléatoire dans l’espace défini
            profondeur = random.uniform(0.10, 0.50)   # Génère une profondeur aléatoire (plus la profondeur est petite plus l'objet est loin)
            self.etoiles.append({"pos": pos, "profondeur": profondeur})

    def draw(self, screen, camera):
        # Permet d'afficher les étoiles inividuellement
        for etoile in self.etoiles:
            parralax_offset = camera.offset * etoile["profondeur"] # Calcule un décalage en fonction de la profondeur
            screen_pos = (etoile["pos"] - parralax_offset) * camera.zoom
            size = camera.zoom * etoile["profondeur"]  # Détermine la taille à afficher selon la postion finale
            scaled_image = pygame.transform.rotozoom(self.image, 0, size)
            new_rect = scaled_image.get_rect(center=(screen_pos.x, screen_pos.y))
            screen.blit(scaled_image, new_rect)  # Dessine l’image de l’étoile à l’écran




