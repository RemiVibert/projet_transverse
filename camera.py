import pygame

class Camera:
    def __init__(self, game):
        self.game = game
        self.zoom = 1
        self.offset = pygame.Vector2(0, 0)
        self.dragging = False
        self.drag_start = pygame.Vector2(0, 0)
        self.drag_offset_start = pygame.Vector2(0, 0)
        self.anchored = True

    def world_pos_to_screen_pos(self, pos):
        return (pos - self.offset) * self.zoom

    def world_rect_to_screen_rect(self, rect):
        new_topleft = self.apply(pygame.Vector2(rect.topleft))
        return pygame.Rect(new_topleft, (rect.width * self.zoom, rect.height * self.zoom))

    def apply(self, pos):
        return (pos - self.offset) * self.zoom

    def set_zoom(self, zoom_factor):
        old_zoom = self.zoom
        self.zoom *= zoom_factor
        self.zoom = max(self.game.zoom_min, min(self.zoom, self.game.zoom_max))


        if self.anchored:
            player_screen_before = self.world_pos_to_screen_pos(self.game.player.pos)
            player_screen_after = self.world_pos_to_screen_pos(self.game.player.pos)
            zoom_offset_diff = (player_screen_after - player_screen_before) / self.zoom
            self.offset += zoom_offset_diff

    def update(self):
        if self.anchored:
            screen_center = pygame.Vector2(self.game.screen.get_size()) / 2
            target_offset = self.game.player.pos - (screen_center / self.zoom)
            # Corriger les valeurs extrêmes de zoom
            if abs(self.zoom) < 0.001:
                self.zoom = 0.001
            elif self.zoom > 100:
                self.zoom = 100
            # lisaage
            smoothing = 0.1
            self.offset += (target_offset - self.offset) * smoothing


