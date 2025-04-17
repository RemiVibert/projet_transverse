import pygame
import math
from camera import Camera
from planet import Planet

G = 6.67
g = 9.81


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_fuel = 100
        self.fuel = 100
        self.max_speed = 1000  # Limite de vitesse maximale (en pixels par seconde)

        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.last_direction = pygame.Vector2(0, -1)

        self.SCALE_FACTOR = 8

        self.image = pygame.image.load('assets/sprites/player/idle.png').convert_alpha()

        self.dragging = False
        self.launch_vector = pygame.Vector2(0, 0)
        self.rect = self.image.get_rect(center=self.pos)


    def update(self, game):
        from game import Game

        # Appliquer la gravité et autres forces
        self.pos += self.velocity * game.dt
        self.rect.center = self.pos

        scaled_width = self.image.get_width() * game.camera.zoom / self.SCALE_FACTOR
        self.radius = scaled_width / 2

        for planet in game.planets:
            direction_x = planet.pos[0] - self.pos[0]
            direction_y = planet.pos[1] - self.pos[1]
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            total_radius = self.radius + planet.radius  # Rayon total (vaisseau + planète)
            if distance > 0:
                force = (planet.masse * G * 100000) / (distance ** 2)
                acceleration_x = force * (direction_x / distance)
                acceleration_y = force * (direction_y / distance)
                self.velocity[0] += acceleration_x * game.dt
                self.velocity[1] += acceleration_y * game.dt
            if distance < total_radius: #calculer la collison
                # Calculer la direction du vaisseau à partir de la planète
                direction = (self.pos - planet.pos).normalize()
                # Déplacer le vaisseau à la périphérie de la planète (juste au bord)
                self.pos = planet.pos + direction * (planet.radius + self.radius)

        # Limiter la vitesse
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)


        # Gestion de la gravité
#        for planet in game.planets:

            # Il faut ajouter ici la physique.
            # Pour cela, on peut modifier le vecteur vitesse du joueur avec self.velocity += ...
            # On peut récupérer les variables de la planète avec planet.pos, planet.masse

    def draw(self, screen, camera):
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        scaled_image = pygame.transform.scale(scaled_image, (scaled_image.get_width() // self.SCALE_FACTOR,scaled_image.get_height() // self.SCALE_FACTOR))

        #direction du drag inverse à la direction
        if self.dragging:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_mouse = camera.offset + mouse_pos / camera.zoom
            direction = world_mouse - self.pos
            self.last_direction = -direction  # Inverser la direction du drag
        else:
            direction = self.velocity if self.velocity.length_squared() > 0.01 else self.last_direction

        angle_deg = direction.angle_to(pygame.Vector2(0, -1))
        rotated_image = pygame.transform.rotate(scaled_image, angle_deg)
        new_rect = rotated_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))
        screen.blit(rotated_image, new_rect)

        #dessine la flèche
        if self.dragging:
            start = camera.world_pos_to_screen_pos(self.pos)
            end = camera.world_pos_to_screen_pos(self.pos + direction)
            pygame.draw.line(screen, (35, 168, 242), start, end, 5)

    def handle_event(self, event, camera):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.Vector2(event.pos)
            screen_pos = camera.world_pos_to_screen_pos(self.pos)
            if (mouse_pos - screen_pos).length() < 30:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            mouse_pos = pygame.Vector2(event.pos)
            world_mouse = camera.offset + mouse_pos / camera.zoom
            self.launch_vector = world_mouse - self.pos
            self.velocity += self.launch_vector * 5
            self.dragging = False