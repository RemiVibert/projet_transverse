import pygame
import random # utilisé pour choisir une couleur aléatoire d'asteroide
import os


class Planet:
    def __init__(self, pos, type, game):
        """
            Initialise une planète.

            Args:
            pos (Vector2): position de la planète
            type (str): type de planète : "{taille-type}" : taille = "petite", "moyenne", "grande" ; type = "terre", "gazeuse", "asteroide"
        """
        self.pos = pygame.math.Vector2(pos)  # Position monde convertie en vecteur
        self.type = type.split('-') # Sépare la chaîne en deux parties : taille et type
        self.taille = self.type[0]
        self.type = self.type[1]
        if self.type == "asteroide":
            nb_fichiers = len(os.listdir('assets/sprites/asteroide'))
            #permet d'ajouter une apparence un peu aléatoire et plus naturelle aux murs d'astéroides
            self.image = random.choice(game.images_asteroide)  # Choisit une image d'astéroïde aléatoire
            self.image = pygame.transform.rotate(self.image, random.randint(0, 360))  # Tourne l'image d'un angle aléatoire
        else:
            self.image = pygame.image.load('assets/sprites/planetes/'+type+'.png').convert_alpha()
        self.original_image = self.image  # Si c'est une planète, aucun effet aléatoire

        self.rect = self.image.get_rect(center=self.pos)
        self.radius = self.rect.width / 2 # Rayon utilisé pour les collisions et la gravité

        if self.type == "asteroide":
            max_offset = self.radius * 0.5  
            self.pos.x += random.uniform(-max_offset, max_offset)
            self.masse = 0 # Les asteroides n'ont pas de masse afin qu'ils n'exercent aucune attraction gravitationnelle
            self.pos.y += random.uniform(-max_offset, max_offset) 
        else:
            self.masse = 200 * (self.radius ** 1.7) #Il faut compenser le fait qu'on soit plus loin du centre de la planète si la planète est plus grande, 20 est la masse de base (= de référence)


    def draw(self, screen, camera):
        # Permet de dessiner correctement la planète à l'écran en fonction du zoom
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))
        screen.blit(scaled_image, new_rect)
