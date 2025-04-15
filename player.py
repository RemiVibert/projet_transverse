import pygame
import math
G = 6.67
g = 9.81

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_fuel = 100
        self.fuel = 100

        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)


        self.image = pygame.image.load('assets/sprites/player/idle.png').convert_alpha() #le convert_alpha permet de rendre le fond transparent et d'optimiser l'image
        self.rect = self.image.get_rect(center=self.pos)

        self.dragging = False # Si le joueur est en train de diriger son vaisseau
        self.launch_vector = pygame.Vector2(0, 0)
    
    def update(self, game):

        self.pos[0] += self.velocity[0] * game.dt
        self.pos[1] += self.velocity[1] * game.dt
        self.rect.center = self.pos[0], self.pos[1]

        for planet in game.planets:
            direction_x = planet.pos[0] - self.pos[0]
            direction_y = planet.pos[1] - self.pos[1]
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if distance > 0:
                force = (planet.masse * G * 5000000) / (distance ** 2)  # J'ai multiplié G par 5000000 pour amplifier l'effet
                acceleration_x = force * (direction_x / distance)
                acceleration_y = force * (direction_y / distance)
                self.velocity[0] += acceleration_x * game.dt
                self.velocity[1] += acceleration_y * game.dt
                print(f"Force: {force}, AccX: {acceleration_x}, AccY: {acceleration_y}")



        # Gestion de la gravité
#        for planet in game.planets:

            # Il faut ajouter ici la physique.
            # Pour cela, on peut modifier le vecteur vitesse du joueur avec self.velocity += ...
            # On peut récupérer les variables de la planète avec planet.pos, planet.masse



            


    def draw(self, screen, camera):
        # appliquer le zoom
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        scaled_image = pygame.transform.scale(scaled_image, (scaled_image.get_width() // 8, scaled_image.get_height() // 8))
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))
        screen.blit(scaled_image, new_rect)

        if self.dragging:
            # Dessiner la flèche
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_mouse = camera.offset + mouse_pos / camera.zoom
            lenght = self.pos - world_mouse
            start = camera.world_pos_to_screen_pos(self.pos)
            end = camera.world_pos_to_screen_pos(self.pos + lenght)
            pygame.draw.line(screen, (35, 168, 242), start, end, 5)
    
    def handle_event(self, event, camera):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # clic gauche
                # Conversion de la position de la souris en coordonnées du monde
                world_mouse = camera.offset + pygame.Vector2(event.pos) / camera.zoom
                if self.rect.collidepoint(world_mouse):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                # Calculer le vecteur de lancement à partir de la position de la souris
                mouse_pos = pygame.Vector2(event.pos)
                world_mouse = camera.offset + mouse_pos / camera.zoom
                self.launch_vector = self.pos - world_mouse
                # Appliquer un facteur de mise à l'échelle pour la vitesse
                self.velocity += self.launch_vector * 5
                self.dragging = False
