import pygame

#Cette classe gère le zoom, le déplacement et le suivi du joueur
class Camera:
    def __init__(self, game):
        self.game = game
        self.zoom = 1 # Niveau de zoom initial à 100%
        self.offset = pygame.Vector2(0, 0)  # Décalage de la caméra
        self.dragging = False # Indique si l'utilisateur est en train de déplacer la caméra à la souris
        self.drag_start = pygame.Vector2(0, 0) # Position de départ du clic de souris
        self.drag_offset_start = pygame.Vector2(0, 0) # Offset de la caméra au moment du clic
        self.anchored = True # Si True, la caméra suit automatiquement le joueur

    def world_pos_to_screen_pos(self, pos): # Convertit une position du monde en position à l’écran, selon l’offset et le zoom
        return (pos - self.offset) * self.zoom

    def world_rect_to_screen_rect(self, rect):
        # Convertit un rectangle du monde en coordonnées écran avec zoom
        new_topleft = self.world_pos_to_screen_pos(pygame.Vector2(rect.topleft))  # Convertit le coin supérieur gauche du rectangle dans les coordonnées écran
        return pygame.Rect(  # Renvoie un rectangle avec taille ajustée selon le zoom
            int(new_topleft.x),
            int(new_topleft.y),
            int(rect.width * self.zoom),
            int(rect.height * self.zoom)
        )

    def set_zoom(self, zoom_factor):
        old_zoom = self.zoom
        self.zoom *= zoom_factor
        self.zoom = max(self.game.zoom_min, min(self.zoom,self.game.zoom_max))  # Limite le zoom

        if self.anchored:
            # Calcule l'ajustement de l'offset pour garder le joueur centré après un zoom
            player_screen_before = (self.game.player.pos - self.offset) * old_zoom
            player_screen_after = (self.game.player.pos - self.offset) * self.zoom
            zoom_offset_diff = (player_screen_before - player_screen_after) / self.zoom
            self.offset += zoom_offset_diff  # Ajuste l’offset pour éviter que le joueur ne saute à l’écran

        # Recentre la caméra sur le joueur après chaque zoom
        self.recenter_on_player()


    def update(self):
        if self.anchored:
            # Calcule l'offset cible pour centrer le joueur à l'écran, puis applique un lissage
            screen_center = pygame.Vector2(self.game.screen.get_size()) / 2
            target_offset = self.game.player.pos - (screen_center / self.zoom)  # Calcule l’offset idéal pour que le joueur reste centré

            distance = (target_offset - self.offset).length()  # Calculer la distance entre la caméra et la position cible


            smoothing = min(0.1 + distance / 1, 0.3)  # Ajuste le lissage selon la distance
            self.offset += (target_offset - self.offset) * smoothing

    def recenter_on_player(self):
        # Recentre immédiatement la caméra sur le joueur
        screen_center = pygame.Vector2(self.game.screen.get_size()) / 2 # Centre de l’écran en pixels
        self.offset = self.game.player.pos - (screen_center / self.zoom) # Replace la caméra de façon à centrer directement le joueur


    def apply(self, obj):
        # Applique la transformation de la caméra à un objet
        return self.world_rect_to_screen_rect(obj.rect)
