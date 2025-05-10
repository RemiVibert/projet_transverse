import pygame
from player import Player
from graphismes import Etoiles
from camera import Camera
import levels
from planet import Planet
from collectible import Collectible
from fuel import Fuel
import json
from base import Base



class Game():
    def __init__(self, screen):
        """
            Permet de gérer les éléments principaux du jeu.

            Args:
                screen (pygame.Surface) : surface d'affichage sur laquelle dessiner les éléments visuels liés au fuel
        """
        self.MAX_DISTANCE_OUT_OF_SPACE = 20_000 # Constante définissant la distance max avant de considérer le joueur comme perdu dans l'espace
        self.screen = screen # Référence vers la surface d'affichage
        self.dt:float = 0 # Temps écoulé entre deux frames
        self.player = Player(self) # Instancie le joueur

        self.min_cam_x = 0
        self.min_cam_y = 0
        self.max_cam_x = 10000
        self.max_cam_y = 10000

        self.camera = Camera(self)

        self.cam_speed = 30  # Vitesse de déplacement manuel de la caméra
        self.zoom = 1  # Facteur de zoom initial (100%)
        self.zoom_speed = 0.1  # Vitesse de changement de zoom
        self.zoom_min = 0.01
        self.zoom_max = 10

        self.levels = []  # Liste des niveaux
        self.niveau_actuel = 0
        self.load_levels()  # Charge les niveaux depuis le fichier JSON

        nb_etoiles = (self.max_cam_x - self.min_cam_x) * (self.max_cam_y - self.min_cam_y) // 500_000 #  # Calcule un nombre d’étoiles basé sur la taille de la carte
        self.etoiles = Etoiles(nb_etoiles, self.max_cam_x*2, self.max_cam_y*2, self.min_cam_x, self.min_cam_y)  # Crée les étoiles avec une zone étendue pour éviter qu’elles disparaissent
        
        self.pressed = {  # Dictionnaire pour gérer l’état des touches fléchées.
            pygame.K_RIGHT: False,
            pygame.K_LEFT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,

        }
        self.end_screen_active = False
        self.end_message = ""  # Message à afficher à la fin
        self.victoire = False
        self.end_background = None
        self.base = None

        level_data = self.levels[self.niveau_actuel]


    def is_pressed(self, key):
        # Retourne l’état d’une touche si elle est surveillée
        if key in self.pressed:
            return self.pressed[key]
        else:
            return False



    def update(self, screen):
        self.keys = pygame.key.get_pressed() # Liste des touches pressées en continu
        pan_speed = 300 * self.dt / self.camera.zoom # Vitesse de déplacement caméra dépendant du temps + zoom

        # Déplacement manuel de la caméra via les touches fléchées
        if not self.camera.anchored:
            if self.keys[pygame.K_LEFT]:
                self.camera.offset.x -= pan_speed
            if self.keys[pygame.K_RIGHT]:
                self.camera.offset.x += pan_speed
            if self.keys[pygame.K_UP]:
                self.camera.offset.y -= pan_speed
            if self.keys[pygame.K_DOWN]:
                self.camera.offset.y += pan_speed
        


        if self.camera.dragging and not self.camera.anchored: # Si la souris est en train de déplacer la caméra
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_delta = ((mouse_pos - self.camera.drag_start) / self.camera.zoom)
            self.camera.offset = self.camera.drag_offset_start - drag_delta # Met à jour l’offset selon le mouvement souris

        self.player.update() # Met à jour le joueur

        for fuel in self.fuels[:]:  # Parcours une copie de la liste pour éviter les problèmes de suppression
            if self.player.rect.colliderect(fuel.rect):
                fuel.collect()  # Collecte le fuel


        #Les différentes conditions de fin de niveau : mort par crash  et win : déclenché dans la gestion des collisions et mort d'out of fuel : declenché dans la gestion du tir

        # Partie qui permet de déterminer si le vaisseau est "out of space"
        if self.planets:
            distance_to_closest_thing = min([self.player.pos.distance_to(planet.pos) for planet in self.planets])
        else:
            distance_to_closest_thing = 1_000_000
            
        closest_thing = min(distance_to_closest_thing, self.player.pos.distance_to(self.base.pos))

        if closest_thing > self.MAX_DISTANCE_OUT_OF_SPACE: # Si le joueur est trop loin de toute planète
            self.game_over("out_of_space", False)

    def load_levels(self):
        with open("levels.json", "r", encoding="utf-8") as f:
            data = json.load(f)  # Charge le contenu du fichier JSON
            self.levels = data["levels"]  # Récupère la liste des niveaux

    def load_level(self, niveau_index=None):
        if niveau_index is None:
            niveau_index = self.niveau_actuel
        level = self.levels[niveau_index]  # Charge le niveau spécifié

        self.cam_x = level["spawn"][0]  # Position caméra x initiale
        self.cam_y = level["spawn"][1]  # Position caméra y initiale

        # Récupère les dimensions du monde à partir du niveau
        self.min_cam_x = level["taille"]["min_x"]
        self.min_cam_y = level["taille"]["min_y"]
        self.max_cam_x = level["taille"]["max_x"]
        self.max_cam_y = level["taille"]["max_y"]

        self.player.pos = pygame.Vector2(level["spawn"])  # Position initiale du joueur
        self.player.max_fuel = level["max_fuel"]
        self.player.fuel = level["start_fuel"]


        self.planets = []  # Liste des planètes dans le niveau
        self.collectibles = []
        self.fuels = []

        base_init = pygame.image.load("assets/sprites/base/base.png").convert_alpha()
        new_width = 800
        new_height = 800
        base_init_resized = pygame.transform.scale(base_init, (new_width, new_height))
        base_x, base_y = level["end"]
        self.base = Base(base_x, base_y, base_init_resized) # Initialise la base de fin de niveau


        for planete in level["planetes"]:
            self.planets.append(Planet(planete["position"],planete["type"]))  # Crée une instance de planète avec sa position et son type

        for collectible in level["collectibles"]:
            self.collectibles.append(
                Collectible(pygame.Vector2(collectible), self))  # Crée une instance de collectible avec sa position

        for fuel in level["carburant"]:
            position = pygame.Vector2(fuel["position"])  # Utilise "position" du carburant
            quantité = fuel["quantité"]  # Récupère la quantité de carburant
            self.fuels.append(Fuel(position, quantité, self))
        self.nb_collectibles = len(self.collectibles)
        pygame.mixer.Sound("assets/audio/spawn_clic.mp3").play()

        self.player.collected_collectibles = 0
        self.total_collectibles = len(level["collectibles"])
        self.camera.recenter_on_player()

    def next_level(self):
        # Passe au niveau suivant et retourne au début si on dépasse le dernier niveau
        self.niveau_actuel = (self.niveau_actuel + 1) % len(self.levels)
        self.load_level()


    def game_over(self, message: str, victoire: bool = False):
        if self.end_screen_active:  # Empêche de la relancer si déjà morte
            return

        print(f"\033[1;31mFIN DU NIVEAU : {message}\033[0m")

        if self.player.godmod and not victoire: # Ignore si godmod activé (debug)
            return
        # Réinitialise les variables du niveau
        self.end_screen_active = True
        self.victoire = victoire
        self.camera.anchored = True
        self.camera.recenter_on_player()
        self.camera.update()
        self.player.velocity = pygame.Vector2(0, 0)
        self.player.has_launched = False
        self.player.dragging = False
        self.player.fuel_cost = None
        self.player.last_direction = pygame.Vector2(0, -1)
        image_path = None

        # Choix de l’image de fin et du son en fonction de la cause de la mort
        if message == "out of fuel":
            image_path = "assets/level_end_screen/dead_no_fuel.png"
            pygame.mixer.Sound("assets/audio/power_down.mp3").play()
        elif message == "out_of_space":
            image_path = "assets/level_end_screen/dead_lost.png"
            pygame.mixer.Sound("assets/audio/power_down.mp3").play()
        elif message == "crash":
            image_path = "assets/level_end_screen/dead_crash.png"
            pygame.mixer.Sound("assets/audio/explode.mp3").play()
        elif message == "win" or victoire:
            victoire = True
            image_path = "assets/level_end_screen/image_fin_niveau.PNG"
            sound = pygame.mixer.Sound("assets/audio/Sekiro - Shinobi Execution sound effect.mp3")
            sound.set_volume(0.2)  # Régle le volume à 20%
            sound.play()
        else:
            msg = "Fin de niveau." # Message par défaut si non reconnu

        # Charge et redimensionne l'image de fin pour affichage
        if image_path:
            death_overlay = pygame.image.load(image_path).convert_alpha()
            self.death_overlay = pygame.transform.scale(death_overlay, (500, 500))

    def show_end_screen(self, message: str, victoire: bool, screen: pygame.Surface, image: pygame.Surface|None = None):
        self.end_screen_active = True # Active l'écran de fin
        self.victoire = victoire
        if image:
            screen.blit(image, (100, 200))

    def check_victory(self):
        if self.end_screen_active or not self.player.has_launched: # Ignore si fin déjà déclenchée ou si le joueur n’a pas été lancé
            return
        if self.base.check_collision(self.player.rect): # type: ignore
            self.game_over("win", victoire=True) # Déclenche la victoire

    def calculate_stars(self):
        # Calcule le nombre d'étoiles à afficher une fois la victoire du niveau déclenchée
        if self.total_collectibles == 0: # Si aucun collectible, accorde directement 3 étoiles
            return 3
        ratio = self.player.collected_collectibles / self.total_collectibles # Calcule le ratio de collectibles récupérés et accorde des étoiles en fonction
        if ratio >= 1.0:
            return 3
        elif ratio >= 2.0 / 3.0:
            return 2
        elif ratio >= 1.0 / 3.0:
            return 1
        else:
            return 0