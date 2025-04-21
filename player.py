import pygame
import math
from camera import Camera
from planet import Planet

G = 6.67 # Constante gravitationnelle
g = 9.81 # Gravité terrestre


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_fuel = 100 # Quantité maximale de carburant
        self.fuel = 100 # Carburant actuel

        self.max_speed = 1000 # Limite de vitesse maximale (en pixels par seconde)
        self.has_launched = False #le joueur n'a jamais été lancé

        self.pos:pygame.Vector2 = pygame.Vector2(0, 0) # Position du vaisseau dans le monde
        self.velocity:pygame.Vector2 = pygame.Vector2(0, 0) # Vitesse actuelle du vaisseau
        self.last_direction:pygame.Vector2 = pygame.Vector2(0, -1) # Dernière direction connue

        self.SCALE_FACTOR = 8  # Constante de mise à l’échelle pour l’affichage du vaisseau

        self.image = pygame.image.load('assets/sprites/player/idle.png').convert_alpha()

        self.dragging = False  # Détermine si le joueur est en train de drag le vaisseau
        self.launch_vector = pygame.Vector2(0, 0) # Vecteur de lancement stocké lors du drag
        self.rect = self.image.get_rect(center=self.pos)  # Rect du sprite


    def update(self, game):

        self.pos += self.velocity * game.dt # Mise à jour de la position selon la vélocité et le temps
        self.rect.center = (int(self.pos.x), int(self.pos.y)) # Mise à jour du rect

        # Calcul du rayon du vaisseau
        scaled_width = self.image.get_width() * game.camera.zoom / self.SCALE_FACTOR
        self.radius = scaled_width / 2

        if self.has_launched: # La gravité et les collisions ne s'appliquent que si le vaisseau a été lancé

            self.pos:pygame.Vector2 = pygame.Vector2(self.pos) # pour s'assurer que c'est un vecteur et non un tuple - solution temporaire - TODO : trouver pourquoi c'est un tuple des fois
            
            # Calcul de la gravité - Non fonctionel, juste un test que je laisse si vous voulez
            # planet:Planet
            # for planet in game.planets:
            #     self.velocity.x += (planet.masse / self.pos.distance_to(planet.pos)) * planet.pos[0] * game.dt
            #     self.velocity.y += (planet.masse / self.pos.distance_to(planet.pos)) * planet.pos[1] * game.dt


            for planet in game.planets:  # Appliquer la gravité de chaque planète
                direction_x = planet.pos[0] - self.pos[0]
                direction_y = planet.pos[1] - self.pos[1]
                distance = self.pos.distance_to(planet.pos) # distance entre le joueur et la planète

                total_radius = self.radius + planet.radius  # Rayon total (vaisseau + planète)

                if distance > 0:
                    force = (planet.masse * G * 1000000) / (distance ** 2) # Force gravitationnelle
                    acceleration_x = force * (direction_x / distance)
                    acceleration_y = force * (direction_y / distance)
                    self.velocity[0] += acceleration_x * game.dt
                    self.velocity[1] += acceleration_y * game.dt

                if distance < total_radius: #calculer la collison
                    direction = (self.pos - planet.pos).normalize() # Calculer la direction du vaisseau à partir de la planète
                    self.pos = planet.pos + direction * (planet.radius + self.radius) # Déplacer le vaisseau à la périphérie de la planète (juste au bord)

        # if self.velocity.length() > self.max_speed: # Limiter la vitesse
        #     self.velocity.scale_to_length(self.max_speed)


        # Gestion de la gravité
#        for planet in game.planets:

            # Il faut ajouter ici la physique.
            # Pour cela, on peut modifier le vecteur vitesse du joueur avec self.velocity += ...
            # On peut récupérer les variables de la planète avec planet.pos, planet.masse

    def draw(self, screen, camera):
        # Applique un zoom avec transformation + réduction de taille
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        scaled_image = pygame.transform.scale(scaled_image, (scaled_image.get_width() // self.SCALE_FACTOR,scaled_image.get_height() // self.SCALE_FACTOR))

        if self.dragging: # Si le joueur est en train de drag, on calcule la direction du tir
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_mouse = camera.offset + mouse_pos / camera.zoom
            direction = world_mouse - self.pos
            self.last_direction = -direction  # Inverser la direction du drag
        else:
            direction = self.velocity if self.velocity.length_squared() > 0.01 else self.last_direction

        angle_deg = direction.angle_to(pygame.Vector2(0, -1)) # Angle avec l’axe vertical
        rotated_image = pygame.transform.rotate(scaled_image, angle_deg) # Rotation du vaisseau
        new_rect = rotated_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos)) # Position sur l’écran
        screen.blit(rotated_image, new_rect) # Affichage du vaisseau

        if self.dragging:  #Affiche la flèche si le drag est en cours
            start = camera.world_pos_to_screen_pos(self.pos)
            end = camera.world_pos_to_screen_pos(self.pos + direction)
            pygame.draw.line(screen, (35, 168, 242), start, end, 5)

    def handle_event(self, event, camera):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Début du drag
            
            mouse_pos = pygame.Vector2(event.pos)
            screen_pos = camera.world_pos_to_screen_pos(self.pos)
            if (mouse_pos - screen_pos).length() < 30:  # Si clic proche du vaisseau
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:  # Fin du drag
            mouse_pos = pygame.Vector2(event.pos)
            world_mouse = camera.offset + mouse_pos / camera.zoom # Coordonnées dans le monde
            self.launch_vector = world_mouse - self.pos # Vecteur de propulsion
            self.velocity += self.launch_vector * 5  # Applique une poussée
            self.dragging = False
            self.has_launched = True #le vaisseau a été lancé une fois