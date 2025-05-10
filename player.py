import pygame
import math
from camera import Camera
from planet import Planet

G = 6.67 # Constante gravitationnelle
g = 9.81 # Gravité terrestre


class Player(pygame.sprite.Sprite):
    """
            Initialise un bouton.

            Args:
            game: référence au jeu pour accéder aux éléments globaux.
    """
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.fuel_empty = False
        self.fuel_empty_time = 0
        self.fuel_empty_delay = 0.5

        self.max_fuel = 100 # Quantité maximale de carburant
        self.fuel = 100 # Carburant actuel
        self.fuel_cost = None
    
        self.collected_collectibles = 0 # Nombre de collectibles ramassés

        self.puissance_tir_max = 8_000
        self.max_speed = 6000 # Limite de vitesse maximale (en pixels par seconde)
        self.has_launched = False #le joueur n'a jamais été lancé
        

        self.pos:pygame.Vector2 = pygame.Vector2(0, 0) # Position du vaisseau dans le monde
        self.velocity:pygame.Vector2 = pygame.Vector2(0, 0) # Vitesse actuelle du vaisseau
        self.last_direction:pygame.Vector2 = pygame.Vector2(0, -1) # Dernière direction connue

        self.SCALE_FACTOR = 8  # Constante de mise à l’échelle pour l’affichage du vaisseau

        self.image = pygame.image.load('assets/sprites/player/idle.png').convert_alpha()

        self.dragging = False  # Détermine si le joueur est en train de drag le vaisseau
        self.launch_vector = pygame.Vector2(0, 0) # Vecteur de lancement stocké lors du drag
        self.rect = self.image.get_rect(center=self.pos)  # Rect du sprite

        self.image_out_of_bounds = pygame.image.load('assets/UI/bound.png').convert_alpha()
        self.rect_out_of_bounds = self.image_out_of_bounds.get_rect(center=self.pos)  # Rect du sprite

        self.godmod = False # Debug, penser à supprimer avant la fin (ça va quand même spa  m la console avec le message de mort histoire de voir si on meurt)


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
                distance = self.pos.distance_to(planet.pos) # distance entre le joueur et la planète
                total_radius = self.radius + planet.radius  # Rayon total (vaisseau + planète)
                
                if planet.type == "gazeuse":
                    if distance < total_radius:
                        # Collision avec une planète gazeuse : ralentir fortement le joueur
                        self.velocity *= 0.95
                        continue
                direction_x = planet.pos[0] - self.pos[0]
                direction_y = planet.pos[1] - self.pos[1]

                if distance > 0:
                    force = (planet.masse * G * 50 ) / (distance ** 2) # Force gravitationnelle
                    acceleration_x = force * (direction_x / distance)
                    acceleration_y = force * (direction_y / distance)
                    self.velocity[0] += acceleration_x * self.game.dt
                    self.velocity[1] += acceleration_y * self.game.dt

                if distance < total_radius: #calculer la collison
                    if planet.type != "gazeuse":
                        self.game.game_over("crash", False)

                        direction = (self.pos - planet.pos).normalize() # Calculer la direction du vaisseau à partir de la planète
                        self.pos = planet.pos + direction * (planet.radius + self.radius) # Déplacer le vaisseau à la périphérie de la planète (juste au bord)

                        self.velocity = self.velocity.reflect(direction) # On reflète la vélocité pour simuler un rebond
                        self.velocity *= 0.8  # On peut aussi réduire un peu la vitesse pour simuler de la perte d'énergie

            # Collection des collectibles
            for collectible in self.game.collectibles:
                if self.rect.colliderect(collectible.rect):
                    collectible.collect()
                    pygame.mixer.Sound("assets/audio/collect.mp3").play()  # Son de collecte



    def draw(self, screen, camera):
        # Applique un zoom avec transformation + réduction de taille
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        scaled_image = pygame.transform.scale(scaled_image, (scaled_image.get_width() // self.SCALE_FACTOR, scaled_image.get_height() // self.SCALE_FACTOR))

        if self.dragging:  # Si le joueur est en train de drag, on calcule la direction du tir
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_mouse = camera.offset + mouse_pos / camera.zoom
            direction = self.pos - world_mouse  # Inverser la direction pour que la flèche pointe à l'opposé

            # Calculer la longueur maximale de la flèche en fonction du carburant disponible
            max_launch_strength = min(self.fuel * 200, 1000)  # 200 pixels de flèche par unité de carburant, max 1000 pixels
            if direction.length() > max_launch_strength:
                direction.scale_to_length(max_launch_strength)

            self.last_direction = direction

            # Calculer le coût en carburant pour la longueur actuelle de la flèche
            self.fuel_cost = int(direction.length() / 200) + 1  # 1 unité de carburant pour 200 pixels de flèche

            # Afficher la flèche
            start = camera.world_pos_to_screen_pos(self.pos)
            segment_length = direction.length() / self.fuel_cost -10 # Longueur de chaque segment
            if direction.length() > 0:
                segment_direction = direction.normalize() * segment_length
            else:
                segment_direction = pygame.Vector2(0, 0)

            for i in range(self.fuel_cost):
                end = camera.world_pos_to_screen_pos(self.pos + segment_direction * (i + 1))
                pygame.draw.line(screen, (35, 168, 242), start, end, 5)
                start = end  # Le début du prochain segment est la fin du précédent

            # Afficher le coût en carburant
            font = pygame.font.Font(None, 36)  # Police par défaut
            text = font.render(f"Fuel Cost: {self.fuel_cost}", True, (255, 255, 255))  # Texte blanc
            text_rect = text.get_rect(bottomright=(screen.get_width() - 10, screen.get_height() - 10))
            screen.blit(text, text_rect)

        else:
            direction = self.velocity if self.velocity.length_squared() > 0.01 else self.last_direction

        angle_deg = direction.angle_to(pygame.Vector2(0, -1))  # Angle avec l’axe vertical
        rotated_image = pygame.transform.rotate(scaled_image, angle_deg)  # Rotation du vaisseau
        new_rect = rotated_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))  # Position sur l’écran
        screen.blit(rotated_image, new_rect)  # Affichage du vaisseau

        # === Afficher la barre de carburant === #
        fuel_bar_height = 500  # Hauteur maximale de la barre
        fuel_bar_width = 50  # Largeur de la barre
        fuel_bar_x = 10  # Position X de la barre
        fuel_bar_y = 100  # Position Y de la barre

        # Calculer la hauteur de la barre en fonction du carburant restant
        current_fuel_height = int((self.fuel / self.max_fuel) * fuel_bar_height)

        # Dessiner le fond de la barre (gris)
        pygame.draw.rect(screen, (50, 50, 50), (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height))

        # Dessiner la barre de carburant (rouge)
        pygame.draw.rect(screen, (255, 0, 0), (fuel_bar_x, fuel_bar_y + (fuel_bar_height - current_fuel_height), fuel_bar_width, current_fuel_height))

        # Charger et redimensionner l'image de carburant une seule fois
        if not hasattr(self, 'fuel_icon'): # Pour vérifier si l'icône a déjà été chargée
            fuel_icon_original = pygame.image.load('assets/UI/carburant.png').convert_alpha()
            self.fuel_icon = pygame.transform.scale(fuel_icon_original, (fuel_bar_width, fuel_bar_width))

        # Afficher l'icône de carburant sous la barre
        icon_x = fuel_bar_x
        icon_y = fuel_bar_y + fuel_bar_height + 5  # Positionner juste en dessous de la barre avec un petit espace
        screen.blit(self.fuel_icon, (icon_x, icon_y))

        # Afficher la diminution prévue
        if self.fuel_cost is not None:
            fuel_apres_tir = max(self.fuel - self.fuel_cost, 0)
            hauteur_diminution = int((fuel_apres_tir / self.max_fuel) * fuel_bar_height)

            # Dessiner la diminution prévue (orange)
            pygame.draw.rect(screen, (255, 165, 0), (
            fuel_bar_x, fuel_bar_y + (fuel_bar_height - current_fuel_height), fuel_bar_width,
            current_fuel_height - hauteur_diminution))

        # Afficher les bordures rouges en plus ou moins transparentes en fonction de la distance du out of bounds
        max_distance = self.game.MAX_DISTANCE_OUT_OF_SPACE
        if self.game.planets:
            closest_distance = min(self.pos.distance_to(planet.pos) for planet in self.game.planets)
        else:
            closest_distance = 1_000_000
        closest_distance = min(closest_distance, self.pos.distance_to(self.game.base.pos))  # Limiter la distance à la distance maximale

        transparency = 255- (max(0, min(255, int(500 * (1 - closest_distance / max_distance)))))  # Calculer la transparence proportionnellement

        self.image_out_of_bounds.set_alpha(transparency)  # Appliquer la transparence
        # new_rect_out_of_bounds = self.image_out_of_bounds.get_rect(center=camera.world_pos_to_screen_pos(self.pos))  # Position sur l’écran
        
        self.rect_out_of_bounds.center = (screen.get_width() // 2, screen.get_height() // 2)  # Centrer sur l'écran
        screen.blit(self.image_out_of_bounds, self.rect_out_of_bounds)  # Affichage du vaisseau

        # Afficher la diminution prévue
        if self.fuel_cost is not None:
            fuel_apres_tir = max(self.fuel - self.fuel_cost, 0)
            hauteur_diminution = int((fuel_apres_tir / self.max_fuel) * fuel_bar_height)

            # Dessiner la diminution prévue (orange)
            pygame.draw.rect(screen, (255, 165, 0), (fuel_bar_x, fuel_bar_y + (fuel_bar_height - current_fuel_height), fuel_bar_width, current_fuel_height - hauteur_diminution))



        


        # === DEBUG === # 
        # Affiche le rect du joueur avec un rectangle rouge transparent
        #rect_surface = pygame.Surface((new_rect.width, new_rect.height), pygame.SRCALPHA)
        #rect_surface.fill((255, 0, 0, 0))  # Rouge transparent # mettre le dernier "0" à 75 pour rendre faire apparaitre
        #screen.blit(rect_surface, new_rect.topleft)


        # === Afficher le nombre de collectibles collectés === #
        font = pygame.font.Font(None, 36)  # Police par défaut
        text = font.render(f"{self.collected_collectibles}/{self.game.nb_collectibles}", True, (255, 255, 255))  # Texte blanc
        # Charger et redimensionner l'image du collectible une seule fois
        if not hasattr(self, 'collectible_icon'):
            collectible_icon_original = pygame.image.load('assets/sprites/collectibles/collectible.png').convert_alpha()
            self.collectible_icon = pygame.transform.scale(collectible_icon_original, (36, 36))

        # Afficher l'icône du collectible à côté du texte
        if self.game.nb_collectibles:  # Afficher seulement si le nombre de collectibles est supérieur à 0
            icon_rect = self.collectible_icon.get_rect(topleft=(10, 10))
            screen.blit(self.collectible_icon, icon_rect)
            text_rect = text.get_rect(topleft=(50, 10))
            screen.blit(text, text_rect)  # Affiche le texte à l'écran

    def handle_event(self, event, camera):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Début du drag
            mouse_pos = pygame.Vector2(event.pos)
            screen_pos = camera.world_pos_to_screen_pos(self.pos)
            if (mouse_pos - screen_pos).length() < 30:  # Si clic proche du vaisseau
                self.dragging = True
            if self.rect.collidepoint(mouse_pos):
                self.velocity = pygame.Vector2(0,0)
                self.angular_velocity = 0
                self.external_forces = pygame.Vector2(0,0)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:  # Fin du drag
            mouse_pos = pygame.Vector2(event.pos)
            world_mouse = camera.offset + mouse_pos / camera.zoom  # Coordonnées dans le monde
            max_launch_strength = min(self.fuel * 200, self.puissance_tir_max)  # Limite de puissance en fonction du carburant
            self.launch_vector = self.pos - world_mouse

            # Limiter la longueur du vecteur de lancement
            if self.launch_vector.length() > max_launch_strength:
                self.launch_vector.scale_to_length(max_launch_strength)

            self.velocity += self.launch_vector * 5  # Applique une poussée
            # Limiter la vitesse au maximum autorisé
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

            pygame.mixer.Sound("assets/audio/woosh.mp3").play()
            self.dragging = False
            self.has_launched = True  # Le vaisseau a été lancé une fois

            # Réduire le carburant en fonction du coût
            if self.fuel_cost is not None:
                self.fuel -= self.fuel_cost
                self.fuel_cost = None
            if self.fuel <= 0 and not self.fuel_empty:
                self.fuel_empty = True
                self.fuel_empty_time = pygame.time.get_ticks() / 1000 #on laisse un délai en ticksdra
            if self.fuel_empty and (pygame.time.get_ticks() / 1000 - self.fuel_empty_time) >= self.fuel_empty_delay:
                self.game.game_over("out of fuel", False)
                self.fuel_empty = False #on réinitialise pour la prochaine partie
