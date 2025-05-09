import pygame

class Base:
    def __init__(self, x, y, image):
        self.image = image
        self.pos = pygame.Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen, camera):
        transformed_rect = camera.apply(self)
        screen.blit(pygame.transform.scale(self.image, transformed_rect.size), transformed_rect.topleft)

    def check_collision(self, player_rect):
        base_rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())
        return base_rect.colliderect(player_rect)

    def get_rect(self):
        width = self.image.get_width()
        height = self.image.get_height()
        return pygame.Rect(self.pos.x, self.pos.y, width, height)