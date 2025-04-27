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

        # Définit la masse gravitationnelle de la planète selon sa taille
        # la masse d'une planète 2x plus grosse devra être + que 2x plus grande, car il faut compenser le fait qu'on soit plus loin du centre de la planète (à cause de la taille de la planète) 
        base_mass = 20
        if self.taille == "petite":
            self.masse = base_mass * (self.radius ** 2)
        elif self.taille == "moyenne":
            self.masse = base_mass * (self.radius ** 2)
        elif self.taille == "grande":
            self.masse = base_mass * (self.radius ** 2)
        else:
            raise ValueError("Taille de la planète non valide")

    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom) # Applique un zoom à l'image de la planète
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Calcule le rectangle de dessin pour que la planète soit centrée correctement
        screen.blit(scaled_image, new_rect) # Affiche l’image de la planète à l’écran
