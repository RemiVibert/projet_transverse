import pygame

class Fuel:
    def __init__(self, pos: pygame.Vector2, charges: int, game):
        """
        Initialise un bidon de fuel.

        Args:
            pos (pygame.Vector2): Position du bidon dans le monde.
            charges (int): Quantité de fuel contenue dans le bidon.
            game: Référence au jeu pour accéder aux éléments globaux.
        """
        self.pos = pos
        self.charges = charges
        self.game = game

        # Déterminer le type de bidon en fonction des charges
        if charges <= 10:
            self.image = pygame.image.load('assets/sprites/carburant/vide.PNG').convert_alpha()
        elif charges <= 30:
            self.image = pygame.image.load('assets/sprites/carburant/plein.PNG').convert_alpha()
        else:
            self.image = pygame.image.load('assets/sprites/carburant/plusieurs.PNG').convert_alpha()

        # Redimensionne l'image pour l'affichag en divisant par 10
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 15))  # Redimensionne l'image


        self.rect = self.image.get_rect(center=self.pos)  # Crée le rectangle de collision
        self.original_image = self.image

    def collect(self):
        self.game.player.fuel = min(self.game.player.fuel + self.charges, self.game.player.max_fuel)  # Ajoute le fuel au joueur sans dépasser le maximum
        pygame.mixer.Sound('assets/audio/refuel.mp3').play()
        self.game.fuels.remove(self)  # Retire le bidon de la liste des fuels

    def draw(self, screen, camera):
        # Affiche le bidon de fuel à l'écran.
        scaled_image = pygame.transform.rotozoom(self.original_image, 0, camera.zoom)  # Applique un zoom à l'image
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))  # Calcule la position à l'écran
        screen.blit(scaled_image, new_rect)  # Affiche l'image
