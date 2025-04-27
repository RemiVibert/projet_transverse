import pygame
import random

class Etoiles(pygame.sprite.Sprite):
    def __init__(self, nb_etoiles, max_x, max_y, min_x, min_y): # Prend en paramètres le nombre d'étoiles et les limites de leur position.
        super().__init__()
        self.image = pygame.image.load("assets/sprites/decor/star.png") # Charge l'image des étoiles
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionne l'image de l’étoile à une taille de 50x50 pixels

        self.etoiles = []  # Initialise une liste vide qui contiendra la postion et profondeur de chaque étoile

        for i in range(nb_etoiles):
            pos = pygame.Vector2(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) # Génère une position aléatoire dans l’espace défini
            profondeur = random.uniform(0.10, 0.50)   # Génère une profondeur aléatoire (plus la profondeur est petite plus l'objet est loin)
            self.etoiles.append({"pos": pos, "profondeur": profondeur}) # Ajoute un dictionnaire représentant l’étoile dans la liste


    def draw(self, screen, camera):
        for etoile in self.etoiles:
            parralax_offset = camera.offset * etoile["profondeur"] # Calcule un décalage en fonction de la profondeur
            screen_pos = (etoile["pos"] - parralax_offset) * camera.zoom  # Calcule la position finale à l’écran
            size = camera.zoom * etoile["profondeur"]  # Détermine la taille à afficher selon la postion finale
            scaled_image = pygame.transform.rotozoom(self.image, 0, size)  # Redimensionne dynamiquement l’image
            new_rect = scaled_image.get_rect(center=(screen_pos.x, screen_pos.y)) # Crée un rectangle centré à la bonne position pour blitter l’image
            screen.blit(scaled_image, new_rect)  # Dessine l’image de l’étoile à l’écran




