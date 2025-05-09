import pygame

class Base:
    def __init__(self, x, y, image):
        self.image = image
        self.pos = pygame.Vector2(x, y)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = pygame.Rect(
            self.rect.x + 300,
            self.rect.y + 300,
            self.rect.width - 600,
            self.rect.height - 600
        )

    def draw(self, screen, camera):
        transformed_rect = camera.apply(self)
        screen.blit(pygame.transform.scale(self.image, transformed_rect.size), transformed_rect.topleft)

    def check_collision(self, player_rect):
        return self.collision_rect.colliderect(player_rect)

    def get_rect(self):
        return self.rect

    def get_collision_rect(self):
        return self.collision_rect
