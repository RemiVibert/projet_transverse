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
        self.max_speed = 15  # Limite la vitesse maximale de déplacement de la caméra

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

            # Calculer la distance entre la caméra et la position cible
            distance = (target_offset - self.offset).length()

            # Limiter la vitesse de rattrapage pour éviter un déplacement trop brutal
            if distance > self.max_speed:
                distance = self.max_speed  # Limite la distance pour éviter le flash

            # Smoothing basé sur la distance restante (en augmentant légèrement si nécessaire)
            smoothing = min(0.1 + distance / 500, 0.3)  # Ajustement dynamique de smoothing
            self.offset += (target_offset - self.offset) * smoothing

    def recenter_on_player(self):
        screen_center = pygame.Vector2(self.game.screen.get_size()) / 2
        self.offset = self.game.player.pos - (screen_center / self.zoom)

    def is_on_screen(self, pos, profondeur=1.0):
        """
        Vérifie si une position est visible à l'écran, en tenant compte de l'effet de parallaxe.
        
        Args:
            pos (pygame.Vector2): Position dans le monde.
            profondeur (float): Facteur de profondeur pour l'effet de parallaxe (1.0 = pas de parallaxe).
        
        Returns:
            bool: True si la position est visible à l'écran, False sinon.
        """
        screen_rect = pygame.Rect(0, 0, self.game.screen.get_width(), self.game.screen.get_height())
        parallax_offset = self.offset * profondeur
        world_pos = (pos - parallax_offset) * self.zoom
        return screen_rect.collidepoint(world_pos)

