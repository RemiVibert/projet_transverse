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
        self.type = type

        # il faudra définir la masse en fonction du type de planète, pour que ça colle avec les calculs de physiques.
        self.masse = ...

        self.image = pygame.image.load('assets/sprites/planetes/'+type+'.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))
        screen.blit(scaled_image, new_rect)