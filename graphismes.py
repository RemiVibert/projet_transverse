import pygame
import random

class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/decor/star.png")
        #changer la taille de l'étoile
        self.plan = random.randint(1, 50)
        self.image = pygame.transform.scale(self.image, ((100 - self.plan)//3, (100 - self.plan)//3))

        self.posx = random.randint(0, 1920)
        self.posy = random.randint(0, 1080)

        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy
    
    def update(self, game):
        self.rect.x = self.posx - game.cam_x // (self.plan + 1)
        self.rect.y = self.posy - game.cam_y // (self.plan + 1)

