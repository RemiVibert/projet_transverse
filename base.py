import pygame

class Base:

    def __init__(self, x, y, image):
        """
            Initialise la base.

            Args:
            x (int) : position en x de la base dans le monde
            y (int) : position en y de la base dans le monde (coordonnée verticale).
            image (pygame.Surface) : image représentant la base.
        """

        self.image = image
        self.pos = pygame.Vector2(x, y)
        self.rect = self.image.get_rect(topleft=(x, y)) # Rectangle de l'image pour gestion de la position
        self.collision_rect = pygame.Rect( # Rectangle de collision avec un offset et des dimensions réduites
            self.rect.x + 300,
            self.rect.y + 300,
            self.rect.width - 600,
            self.rect.height - 600
        )

    def draw(self, screen, camera):
        # Applique la transformation de la caméra à la base pour l'afficher correctement
        transformed_rect = camera.apply(self)
        screen.blit(pygame.transform.scale(self.image, transformed_rect.size), transformed_rect.topleft)

    def check_collision(self, player_rect):
        # Vérifie si le rectangle de collision de la base entre en contact avec celui du joueur
        return self.collision_rect.colliderect(player_rect)

    def get_rect(self):
        # Retourne le rectangle de l'image
        return self.rect

    def get_collision_rect(self):
        # Retourne le rectangle de collision
        return self.collision_rect
