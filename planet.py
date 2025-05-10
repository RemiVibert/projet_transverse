import pygame
import random # utilisé pour choisir une couleur aléatoire d'asteroide
import os
class Planet:
    def __init__(self, pos, type):
        """
            Initialise une planète.

            Args:
            pos (Vector2): position de la planète
            type (str): type de planète : "{taille-type}" : taille = "petite", "moyenne", "grande" ; type = "terre", "gazeuse", "asteroide"
        """
        self.pos = pygame.math.Vector2(pos)  # Position monde convertie en vecteur
        self.type = type.split('-') # Sépare la chaîne en deux parties : taille et type
        self.taille = self.type[0] # Extrait la taille
        self.type = self.type[1] # Extrait le type
        if self.type == "asteroide":
            nb_fichiers = len(os.listdir('assets/sprites/asteroide'))
            self.image = pygame.image.load(f'assets/sprites/asteroide/x-asteroide{random.randint(1, nb_fichiers)}.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() // 20, self.image.get_height() // 20))  # Redimensionne l'image
            self.image = pygame.transform.rotate(self.image, random.randint(0, 360))  # Tourne l'image d'un angle aléatoire
        else:
            self.image = pygame.image.load('assets/sprites/planetes/'+type+'.png').convert_alpha()
        self.original_image = self.image  # Garde l’image de base pour les rescalings

        self.rect = self.image.get_rect(center=self.pos) # Crée un rectangle de collision
        self.radius = self.rect.width / 2  # Rayon monde, sans zoom # Rayon utilisé pour les collisions et la gravité

        if self.type == "asteroide":
            max_offset = self.radius * 0.5  
            self.pos.x += random.uniform(-max_offset, max_offset)
            self.masse = 0
            self.pos.y += random.uniform(-max_offset, max_offset) 
        else:
            self.masse = 200 * (self.radius ** 1.7) #il faut compenser le fait qu'on soit plus loin du centre de la planète si la planète est plus grande, 20 est la masse de base (= de référence)


    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom) # Applique un zoom à l'image de la planète
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Calcule le rectangle de dessin pour que la planète soit centrée correctement
        screen.blit(scaled_image, new_rect) # Affiche l’image de la planète à l’écran
