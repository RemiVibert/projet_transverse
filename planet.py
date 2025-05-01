import pygame


class Planet:
    def __init__(self, pos, type):
        """

                Args:
                    pos (Vector2): position de la planète
                    masse (int): masse de la planète
                    type (str): type de planète : "{taille-type}" : taille = "petite", "moyenne", "grande" ; type = "terre", "gazeuse", "asteroide"
                """
        self.pos = pos  # Position monde
        self.type = type.split('-') # Sépare la chaîne en deux parties : taille et type
        self.taille = self.type[0] # Extrait la taille
        self.type = self.type[1] # Extrait le type

        self.image = pygame.image.load('assets/sprites/planetes/'+type+'.png').convert_alpha()
        self.original_image = self.image  # Garde l’image de base pour les rescalings

        self.rect = self.image.get_rect(center=self.pos) # Crée un rectangle de collision
        self.radius = self.rect.width / 2  # Rayon monde, sans zoom # Rayon utilisé pour les collisions et la gravité

        self.masse = 200 * (self.radius ** 1.7) #il faut compenser le fait qu'on soit plus loin du centre de la planète si la planète est plus grande, 20 est la masse de base (= de référence)


    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom) # Applique un zoom à l'image de la planète
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Calcule le rectangle de dessin pour que la planète soit centrée correctement
        screen.blit(scaled_image, new_rect) # Affiche l’image de la planète à l’écran
