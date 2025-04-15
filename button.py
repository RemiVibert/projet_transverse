import pygame


import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=30, bg_color=(255, 0, 0), text_color=(255, 255, 255), camera=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color
        self.camera = camera
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        scaled_pos = pygame.Vector2(pos[0] / self.camera.zoom, pos[1] / self.camera.zoom)
        return self.rect.collidepoint(scaled_pos)
