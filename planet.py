import pygame


class Planet:
    def __init__(self, pos, type):
        """

                Args:
                    pos (Vector2): position de la planète
                    masse (int): masse de la planète
                    type (str): type de planète : "{taille-type}" : taille = "petite", "moyenne", "grande" ; type = "terre", "gazeuse", "asteroide"
                """
        self.pos = pos
        self.type = type.split('-')
        self.taille = self.type[0]
        self.type = self.type[1]

        self.image = pygame.image.load('assets/sprites/planetes/'+type+'.png').convert_alpha()
        self.original_image = self.image  # Garde l’image de base pour les rescalings

        self.rect = self.image.get_rect(center=self.pos)
        self.radius = self.rect.width / 2  # ← Rayon monde, sans zoom

        if self.taille == "petite":
            self.masse = 10
        elif self.taille == "moyenne":
            self.masse = 50
        elif self.taille == "grande":
            self.masse = 100
        else:
            raise ValueError("Taille de la planète non valide")

    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))
        screen.blit(scaled_image, new_rect)
