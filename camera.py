import pygame

class Camera: # Gère le zoom, le déplacement et le suivi du joueur
    def __init__(self, game):
        self.game = game
        self.zoom = 1 # Niveau de zoom initial (1 = 100%)
        self.offset = pygame.Vector2(0, 0) # Décalage de la caméra dans le monde
        self.dragging = False # Indique si l'utilisateur est en train de déplacer la caméra à la souris
        self.drag_start = pygame.Vector2(0, 0) # Position de départ du clic de souris
        self.drag_offset_start = pygame.Vector2(0, 0) # Offset de la caméra au moment du clic
        self.anchored = True # Si True, la caméra suit automatiquement le joueur

    def world_pos_to_screen_pos(self, pos): # Convertit une position du monde en position à l’écran, selon l’offset et le zoom
        return (pos - self.offset) * self.zoom

    def world_rect_to_screen_rect(self, rect):
        new_topleft = self.world_pos_to_screen_pos(pygame.Vector2(rect.topleft))  # Convertit le coin supérieur gauche du rectangle dans les coordonnées écran
        return pygame.Rect(  # Renvoie un nouveau rectangle avec une taille adaptée
            int(new_topleft.x),
            int(new_topleft.y),
            int(rect.width * self.zoom),
            int(rect.height * self.zoom)
        )

    def set_zoom(self, zoom_factor):
        old_zoom = self.zoom  # Sauvegarde du zoom actuel
        self.zoom *= zoom_factor  # Applique le facteur de zoom
        self.zoom = max(self.game.zoom_min, min(self.zoom,self.game.zoom_max))  # Clamp le zoom entre des valeurs minimales et maximales définies

        if self.anchored:
            player_screen_before = (self.game.player.pos - self.offset) * old_zoom  # Position écran du joueur avant le zoom
            player_screen_after = (self.game.player.pos - self.offset) * self.zoom  # Position écran du joueur après le zoom
            zoom_offset_diff = (player_screen_before - player_screen_after) / self.zoom  # Calcule la différence de position à compenser
            self.offset += zoom_offset_diff  # Ajuste l’offset pour éviter que le joueur ne saute à l’écran

        # Recentre la caméra sur le joueur après chaque zoom
        self.recenter_on_player()


    def update(self):
        if self.anchored:
            screen_center = pygame.Vector2(self.game.screen.get_size()) / 2  # Centre de l’écran en pixels
            target_offset = self.game.player.pos - (screen_center / self.zoom)  # Calcule l’offset idéal pour que le joueur reste centré

            distance = (target_offset - self.offset).length()  # Calculer la distance entre la caméra et la position cible


            smoothing = min(0.1 + distance / 1, 0.3)  # Ajuste un facteur de lissage dynamique selon la distance
            self.offset += (target_offset - self.offset) * smoothing # Déplacement progressif vers l’offset cible

    def recenter_on_player(self):
        screen_center = pygame.Vector2(self.game.screen.get_size()) / 2 # Centre de l’écran en pixels
        self.offset = self.game.player.pos - (screen_center / self.zoom) # Replace la caméra de façon à centrer directement le joueur


    def apply(self, obj):
        return self.world_rect_to_screen_rect(obj.rect)
