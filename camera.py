import pygame
class Camera:
    def __init__(self,game):
        self.game = game
        self.zoom = 1
        self.offset = pygame.Vector2(0, 0)
        self.dragging = False
        self.drag_start = pygame.Vector2(0, 0)
        self.drag_offset_start = pygame.Vector2(0, 0)
    
    def world_pos_to_screen_pos(self, pos):
        """Convertir une position du monde en position à l'écran"""
        return (pos - self.offset) * self.zoom
    
    def world_rect_to_screen_rect(self, rect):
        """Convertir un rectangle du monde en rectangle à l'écran"""
        new_topleft = self.apply(pygame.Vector2(rect.topleft))
        return pygame.Rect(new_topleft, (rect.width * self.zoom, rect.height * self.zoom))
    
    def set_zoom(self, zoom_factor):
        self.zoom *= zoom_factor
        # On limite le zoom pour éviter des valeurs extrêmes
        self.zoom = max(self.game.zoom_min, min(self.zoom, self.game.zoom_max))