import pygame
from player import Player
from graphismes import Etoiles
from camera import Camera
import levels
from planet import Planet



class Game():
    def __init__(self):
        self.dt = None # Delta time, temps écoulé depuis la dernière frame
        self.player = Player()
        self.camera = Camera(self)

        self.level = self.load_level(levels.level1)

        self.cam_speed = 30
        self.zoom = 1
        self.zoom_speed = 0.1
        self.zoom_min = 0.01 # Ne pas mettre négatif ou nul
        self.zoom_max = 10

        nb_etoiles = (self.max_cam_x - self.min_cam_x) * (self.max_cam_y - self.min_cam_y) // 5000000 # pour la valeur finale il faudra diviser par ~50000, mais il faudra ajouter un truc pour éviter le lag, là c'est chaud. Plus le nombre est grand, moins ça lag
        self.etoiles = Etoiles(nb_etoiles, self.max_cam_x*2, self.max_cam_y*2, self.min_cam_x, self.min_cam_y)



        self.pressed = {
            pygame.K_RIGHT: False,
            pygame.K_LEFT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,

        }

        
    def is_pressed(self, key):
        if key in self.pressed:
            return self.pressed[key]
        else:
            return False




    def update(self, screen):
        self.dt = pygame.time.Clock().tick(60) / 1000 # On récupère le temps écoulé depuis la dernière frame, pour ne pas impacter la vitesse du jeu en fonction du framerate
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.camera.set_zoom(1.1)
                else:
                    self.camera.set_zoom(0.9)
            
            self.player.handle_event(event, self.camera)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    world_mouse = self.camera.offset + pygame.Vector2(event.pos) / self.camera.zoom
                    if not self.player.rect.collidepoint(world_mouse):
                        self.camera.dragging = True
                        self.camera.anchored = False
                        self.camera.drag_start = pygame.Vector2(event.pos)
                        self.camera.drag_offset_start = self.camera.offset.copy()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.camera.dragging = False

        self.keys = pygame.key.get_pressed()
        pan_speed = 300 * self.dt / self.camera.zoom
        if self.keys[pygame.K_LEFT]:
            self.camera.offset.x -= pan_speed
        if self.keys[pygame.K_RIGHT]:
            self.camera.offset.x += pan_speed
        if self.keys[pygame.K_UP]:
            self.camera.offset.y -= pan_speed
        if self.keys[pygame.K_DOWN]:
            self.camera.offset.y += pan_speed
        
        if self.keys[pygame.K_SPACE]:
            self.camera.anchored = not self.camera.anchored

        if self.camera.anchored:
            self.camera.offset = self.player.rect.center - pygame.Vector2(screen.get_size()) / 2 / self.camera.zoom
        elif self.camera.dragging:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            drag_delta = ((mouse_pos - self.camera.drag_start) / self.camera.zoom)
            self.camera.offset = self.camera.drag_offset_start - drag_delta

        self.player.update(self)
        
        
    def load_level(self, level):
        """
        Charge un niveau.
        """

        self.cam_x = level["spawn"][0]
        self.cam_y = level["spawn"][1]

        self.min_cam_x = level["taille"]["min_x"]
        self.min_cam_y = level["taille"]["min_y"]
        self.max_cam_x = level["taille"]["max_x"]
        self.max_cam_y = level["taille"]["max_y"]

        self.player.pos = pygame.Vector2(level["spawn"])
        
        self.planets = []
        for planete in level["planetes"]:
            self.planets.append(Planet(planete["position"], planete["type"]))