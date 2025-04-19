import pygame
from player import Player
from graphismes import Etoiles
from camera import Camera
import levels
from planet import Planet

class Game():
    def __init__(self, screen):
        self.screen = screen # Référence vers la surface d'affichage
        self.dt = None # Temps écoulé entre deux frames
        self.player = Player() # Instancie le joueur
        self.camera = Camera(self) # Crée la caméra et lui donne accès au contexte du jeu

        self.level = self.load_level(levels.level1) # Charge le niveau actuel à partir du module "levels"

        self.cam_speed = 30 # Vitesse de déplacement manuel de la caméra
        self.zoom = 1 # Facteur de zoom initial
        self.zoom_speed = 0.1 # Vitesse de changement de zoom
        self.zoom_min = 0.01 # Zoom minimal autorisé
        self.zoom_max = 10 # Zoom maximal autorisé

        nb_etoiles = (self.max_cam_x - self.min_cam_x) * (self.max_cam_y - self.min_cam_y) // 500000 #  # Calcule un nombre d’étoiles basé sur la taille de la carte
        self.etoiles = Etoiles(nb_etoiles, self.max_cam_x*2, self.max_cam_y*2, self.min_cam_x, self.min_cam_y)  # Crée les étoiles avec une zone étendue pour éviter qu’elles disparaissent

        self.pressed = {  # Dictionnaire pour gérer l’état des touches fléchées.
            pygame.K_RIGHT: False,
            pygame.K_LEFT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,

        }

        
    def is_pressed(self, key): # Retourne l’état d’une touche si elle est surveillée
        if key in self.pressed:
            return self.pressed[key]
        else:
            return False




    def update(self, screen):
        self.dt = pygame.time.Clock().tick(60) / 1000 # On récupère le temps écoulé depuis la dernière frame, pour ne pas impacter la vitesse du jeu en fonction du framerate
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL: # Gestion du zoom via la molette
                if event.y > 0:
                    self.camera.set_zoom(1.1) # Zoom avant
                else:
                    self.camera.set_zoom(0.9) # Zoom arrière
            
            self.player.handle_event(event, self.camera) # Délègue les événements clavier/souris au joueur

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic gauche
                    world_mouse = self.camera.offset + pygame.Vector2(event.pos) / self.camera.zoom # Convertit la position souris écran en position dans le monde.
                    if not self.player.rect.collidepoint(world_mouse):   # Si clic hors du joueur, active le déplacement libre de la caméra
                        self.camera.dragging = True
                        self.camera.anchored = False
                        self.camera.drag_start = pygame.Vector2(event.pos)
                        self.camera.drag_offset_start = self.camera.offset.copy()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.camera.dragging = False # Arrêt du déplacement libre à la souris

        self.keys = pygame.key.get_pressed() # Liste des touches pressées en continu
        pan_speed = 300 * self.dt / self.camera.zoom # Vitesse de déplacement caméra dépendant du temps + zoom

        # Déplacement manuel de la caméra via les touches fléchées
        if self.keys[pygame.K_LEFT]:
            self.camera.offset.x -= pan_speed
        if self.keys[pygame.K_RIGHT]:
            self.camera.offset.x += pan_speed
        if self.keys[pygame.K_UP]:
            self.camera.offset.y -= pan_speed
        if self.keys[pygame.K_DOWN]:
            self.camera.offset.y += pan_speed
        
        if self.keys[pygame.K_SPACE]:
            self.camera.anchored = not self.camera.anchored  # Active/désactive le suivi automatique du joueur

        elif self.camera.dragging: # Si la souris est en train de déplacer la caméra
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_delta = ((mouse_pos - self.camera.drag_start) / self.camera.zoom)
            self.camera.offset = self.camera.drag_offset_start - drag_delta # Met à jour l’offset selon le mouvement souris

        self.player.update(self) # Met à jour le joueur
        
        
    def load_level(self, level):
        """
        Charge un niveau.
        """

        self.cam_x = level["spawn"][0] # Position caméra x initiale
        self.cam_y = level["spawn"][1] # Position caméra y initiale

        # Récupère les dimensions du monde à partir du niveau
        self.min_cam_x = level["taille"]["min_x"]
        self.min_cam_y = level["taille"]["min_y"]
        self.max_cam_x = level["taille"]["max_x"]
        self.max_cam_y = level["taille"]["max_y"]

        self.player.pos = pygame.Vector2(level["spawn"]) # Position initiale du joueur
        
        self.planets = [] # Liste des planètes dans le niveau

        for planete in level["planetes"]:
            self.planets.append(Planet(planete["position"], planete["type"])) # Crée une instance de planète avec sa position et son type