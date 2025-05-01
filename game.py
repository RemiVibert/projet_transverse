import pygame
from player import Player
from graphismes import Etoiles
from camera import Camera
import levels
from planet import Planet
from collectible import Collectible


MAX_DISTANCE_OUT_OF_SPACE = 20_000

class Game():
    def __init__(self, screen):
        self.screen = screen # Référence vers la surface d'affichage
        self.dt:float = 0 # Temps écoulé entre deux frames
        self.player = Player(self) # Instancie le joueur

        self.load_level(levels.level1) # Charge le niveau actuel à partir du module "levels"
        self.camera = Camera(self)

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
        self.keys = pygame.key.get_pressed() # Liste des touches pressées en continu
        pan_speed = 300 * self.dt / self.camera.zoom # Vitesse de déplacement caméra dépendant du temps + zoom

        # === Déplacement manuel de la caméra via les touches fléchées === #
        if not self.camera.anchored:
            if self.keys[pygame.K_LEFT]:
                self.camera.offset.x -= pan_speed
            if self.keys[pygame.K_RIGHT]:
                self.camera.offset.x += pan_speed
            if self.keys[pygame.K_UP]:
                self.camera.offset.y -= pan_speed
            if self.keys[pygame.K_DOWN]:
                self.camera.offset.y += pan_speed
        


        if self.camera.dragging: # Si la souris est en train de déplacer la caméra
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_delta = ((mouse_pos - self.camera.drag_start) / self.camera.zoom)
            self.camera.offset = self.camera.drag_offset_start - drag_delta # Met à jour l’offset selon le mouvement souris

        self.player.update() # Met à jour le joueur

        # === Conditions de fin de niveau === #

        # mort par crash : déclenché dans la gestion des collisions
        # mort d'out of fuel : declenché dans la gestion du tir
        # win : déclenché dans la gestion des collisions

        # Out of space
        if all(self.player.pos.distance_to(planet.pos) >= planet.radius + MAX_DISTANCE_OUT_OF_SPACE for planet in self.planets):
            self.game_over("out_of_space", False)
        
        
        
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
        
        self.planets:list[Planet] = [] # Liste des planètes dans le niveau

        self.collectibles = []
        for collectible in level["collectibles"]:
            self.collectibles.append(Collectible(pygame.Vector2(collectible), self)) # Crée une instance de collectible avec sa position

        for planete in level["planetes"]:
            self.planets.append(Planet(planete["position"], planete["type"])) # Crée une instance de planète avec sa position et son type

    
    def game_over(self, message:str, victoire:bool = False):
        """
        Déclenche le menu de fin de niveau (victoire ou défaite) correspondant au message. 
        Messages possibles :
        - "out_of_space"
        - "out_of_fuel"
        - "crash"
        - "win" (pas besoin en soit, la variable victoire est suffisante)
        """
        print(message)
        if self.player.godmod:
            return
        
        raise NotImplementedError("Menu de fin de niveau pas encore implémenté") # Avant de supprimer ça, va jeter un oeil au player.godmod