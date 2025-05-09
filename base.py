import pygame

class Base:
    def __init__(self, x, y, image):
        self.image = image
        self.pos = pygame.Vector2(x, y)
        original_rect = self.image.get_rect(center=(x, y))
        reduction = 260

        self.rect = pygame.Rect(
            original_rect.x + reduction // 2,
            original_rect.y + reduction // 2,
            original_rect.width - reduction,
            original_rect.height - reduction
        )


    def draw(self, screen, camera):
        transformed_rect = camera.apply(self)
        screen.blit(pygame.transform.scale(self.image, transformed_rect.size), transformed_rect.topleft)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    def get_rect(self):
        return self.rect