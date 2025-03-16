import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_fuel = 100
        self.fuel = 100

        self.pos_x = 100
        self.pos_y = 100

        self.speed_x = 0
        self.speed_y = 0

        self.speed = 1



        self.image = pygame.image.load('assets/sprites/player/idle.png')
        self.rect = self.image.get_rect()
    
    def update(self, game):
        if game.is_pressed(pygame.K_z):
            self.speed_y -= self.speed
        if game.is_pressed(pygame.K_s):
            self.speed_y += self.speed
        if game.is_pressed(pygame.K_q):
            self.speed_x -= self.speed
        if game.is_pressed(pygame.K_d):
            self.speed_x += self.speed

        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.rect.x = self.pos_x - game.cam_x
        self.rect.y = self.pos_y - game.cam_y