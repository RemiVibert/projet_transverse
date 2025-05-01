import pygame
import math
from camera import Camera
from planet import Planet

G = 6.67 # Constante gravitationnelle
g = 9.81 # Gravité terrestre


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.max_fuel = 100 # Quantité maximale de carburant
        self.fuel = 100 # Carburant actuel
        self.collected_collectibles = 0 # Nombre de collectibles ramassés

        self.max_speed = 20000 # Limite de vitesse maximale (en pixels par seconde)
        self.has_launched = False #le joueur n'a jamais été lancé
        

        self.pos:pygame.Vector2 = pygame.Vector2(0, 0) # Position du vaisseau dans le monde
        self.velocity:pygame.Vector2 = pygame.Vector2(0, 0) # Vitesse actuelle du vaisseau
        self.last_direction:pygame.Vector2 = pygame.Vector2(0, -1) # Dernière direction connue

        self.SCALE_FACTOR = 8  # Constante de mise à l’échelle pour l’affichage du vaisseau

        self.image = pygame.image.load('assets/sprites/player/idle.png').convert_alpha()

        self.dragging = False  # Détermine si le joueur est en train de drag le vaisseau
        self.launch_vector = pygame.Vector2(0, 0) # Vecteur de lancement stocké lors du drag
        self.rect = self.image.get_rect(center=self.pos)  # Rect du sprite

        self.godmod = False # Debug, penser à supprimer avant la fin (ça va quand même spam la console avec le message de mort histoire de voir si on meurt)


    def update(self):

        if self.dragging:
            self.pos += (self.velocity)/3 * self.game.dt # on met un effet de ralentit quand on drag
        else :
            self.pos += self.velocity * self.game.dt

        self.rect.center = (int(self.pos.x), int(self.pos.y)) # Mise à jour du rect

        # Calcul du rayon du vaisseau
        scaled_width = self.image.get_width() * self.game.camera.zoom / self.SCALE_FACTOR
        self.radius = scaled_width / 2

        if self.has_launched: # La gravité et les collisions ne s'appliquent que si le vaisseau a été lancé

            self.pos:pygame.Vector2 = pygame.Vector2(self.pos) # pour s'assurer que c'est un vecteur et non un tuple - solution temporaire - TODO : trouver pourquoi c'est un tuple des fois
            
            # Calcul de la gravité - Non fonctionel, juste un test que je laisse si vous voulez
            # planet:Planet
            # for planet in game.planets:
            #     self.velocity.x += (planet.masse / self.pos.distance_to(planet.pos)) * planet.pos[0] * game.dt
            #     self.velocity.y += (planet.masse / self.pos.distance_to(planet.pos)) * planet.pos[1] * game.dt


            for planet in self.game.planets:  # Appliquer la gravité de chaque planète
                direction_x = planet.pos[0] - self.pos[0]
                direction_y = planet.pos[1] - self.pos[1]
                distance = self.pos.distance_to(planet.pos) # distance entre le joueur et la planète

                total_radius = self.radius + planet.radius  # Rayon total (vaisseau + planète)

                if distance > 0:
                    force = (planet.masse * G * 50 ) / (distance ** 2) # Force gravitationnelle
                    acceleration_x = force * (direction_x / distance)
                    acceleration_y = force * (direction_y / distance)
                    self.velocity[0] += acceleration_x * self.game.dt
                    self.velocity[1] += acceleration_y * self.game.dt

                if distance < total_radius: #calculer la collison
                    self.game.game_over("crash", False)

                    direction = (self.pos - planet.pos).normalize() # Calculer la direction du vaisseau à partir de la planète
                    self.pos = planet.pos + direction * (planet.radius + self.radius) # Déplacer le vaisseau à la périphérie de la planète (juste au bord)

                    self.velocity = self.velocity.reflect(direction) # On reflète la vélocité pour simuler un rebond
                    self.velocity *= 0.8  # On peut aussi réduire un peu la vitesse pour simuler de la perte d'énergie

            # === Collection des collectibles === #
            for collectible in self.game.collectibles:
                if self.rect.colliderect(collectible.rect):
                    collectible.collect()
                    self.collected_collectibles += 1  # Incrémente le nombre de collectibles ramassés



    def draw(self, screen, camera):
        # Applique un zoom avec transformation + réduction de taille
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        scaled_image = pygame.transform.scale(scaled_image, (scaled_image.get_width() // self.SCALE_FACTOR, scaled_image.get_height() // self.SCALE_FACTOR))

        if self.dragging:  # Si le joueur est en train de drag, on calcule la direction du tir
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_mouse = camera.offset + mouse_pos / camera.zoom
            direction = self.pos - world_mouse  # Inverser la direction pour que la flèche pointe à l'opposé
            self.last_direction = direction
        else:
            direction = self.velocity if self.velocity.length_squared() > 0.01 else self.last_direction

        angle_deg = direction.angle_to(pygame.Vector2(0, -1))  # Angle avec l’axe vertical
        rotated_image = pygame.transform.rotate(scaled_image, angle_deg)  # Rotation du vaisseau
        new_rect = rotated_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))  # Position sur l’écran
        screen.blit(rotated_image, new_rect)  # Affichage du vaisseau

        if self.dragging:  # Affiche la flèche si le drag est en cours
            start = camera.world_pos_to_screen_pos(self.pos)
            end = camera.world_pos_to_screen_pos(self.pos + direction)
            pygame.draw.line(screen, (35, 168, 242), start, end, 5)

        # === DEBUG === # 
        # Affiche le rect du joueur avec un rectangle rouge transparent
        rect_surface = pygame.Surface((new_rect.width, new_rect.height), pygame.SRCALPHA)
        rect_surface.fill((255, 0, 0, 0))  # Rouge transparent # mettre le dernier "0" à 75 pour rendre faire apparaitre
        screen.blit(rect_surface, new_rect.topleft)


        # === Afficher le nombre de collectibles collectés === #
        font = pygame.font.Font(None, 36)  # Police par défaut
        text = font.render(f"Collectibles: {self.collected_collectibles}", True, (255, 255, 255))  # Texte blanc
        text_rect = text.get_rect(topleft=(10, 10))
        screen.blit(text, text_rect)  # Affiche le texte à l'écran

    def handle_event(self, event, camera):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Début du drag
            mouse_pos = pygame.Vector2(event.pos)
            screen_pos = camera.world_pos_to_screen_pos(self.pos)
            if (mouse_pos - screen_pos).length() < 30:  # Si clic proche du vaisseau
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:  # Fin du drag
            mouse_pos = pygame.Vector2(event.pos)
            world_mouse = camera.offset + mouse_pos / camera.zoom  # Coordonnées dans le monde
            max_launch_strength = 1000  # Valeur max de puissance
            self.launch_vector = self.pos - world_mouse  # Inverser la direction pour que le vaisseau parte dans la direction indiquée
            # On limite la longueur du vecteur
            if self.launch_vector.length() > max_launch_strength:
                self.launch_vector.scale_to_length(max_launch_strength)
            self.velocity += self.launch_vector * 5  # Applique une poussée
            # Limiter la vitesse au maximum autorisé
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
            self.dragging = False
            self.has_launched = True  # Le vaisseau a été lancé une fois