import pygame
from player import Player
from graphismes import Etoile

class Game():
    def __init__(self):
        self.player = Player()
        self.cam_x = 0
        self.cam_y = 0
        self.min_cam_x = -2000
        self.min_cam_y = -2000
        self.max_cam_x = 2000
        self.max_cam_y = 2000
        self.cam_speed = 30

        self.pressed = {
            pygame.K_RIGHT: False,
            pygame.K_LEFT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,

        }

        self.etoiles = pygame.sprite.Group()
        for i in range(100):
            self.etoiles.add(Etoile())
        
    def is_pressed(self, key):
        if key in self.pressed:
            return self.pressed[key]
        else:
            return False


    def update(self):
        if self.is_pressed(pygame.K_RIGHT):
            self.cam_x += self.cam_speed
        if self.is_pressed(pygame.K_LEFT):
            self.cam_x -= self.cam_speed
        if self.is_pressed(pygame.K_UP):
            self.cam_y -= self.cam_speed
        if self.is_pressed(pygame.K_DOWN):
            self.cam_y += self.cam_speed

        self.player.update(self)
        for etoile in self.etoiles:
            etoile.update(self)
        
        
