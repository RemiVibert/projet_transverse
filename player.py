import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_fuel = 100
        self.fuel = 100

        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)


        self.image = pygame.image.load('assets/sprites/player/idle.png').convert_alpha() #le convert_alpha permet de rendre le fond transparent et d'optimiser l'image
        self.rect = self.image.get_rect(center=self.pos)

        self.dragging = False # Si le joueur est en train de diriger son vaisseau
        self.launch_vector = pygame.Vector2(0, 0)
    
    def update(self, game):
        # ↓ Uniquement pour debug ↓
        # Les contrôles du joueur s'effectue avec un "tir de golf, ici on ajoute le zqsd"
        if game.is_pressed(pygame.K_z):
            self.pos.y -= 10
        if game.is_pressed(pygame.K_s):
            self.pos.y += 10
        if game.is_pressed(pygame.K_q):
            self.pos.x -= 10
        if game.is_pressed(pygame.K_d):
            self.pos.x += 10
        # ↑ Uniquement pour debug ↑


        self.pos += self.velocity * game.dt
        self.rect.center = self.pos
    
    def draw(self, screen, camera):
        # appliquer le zoom
        scaled_image = pygame.transform.rotozoom(self.image, 0, camera.zoom)
        new_rect = scaled_image.get_rect(center=camera.world_pos_to_screen_pos(self.pos))
        screen.blit(scaled_image, new_rect)

        if self.dragging:
            # Dessiner la flèche
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            world_mouse = camera.offset + mouse_pos / camera.zoom
            lenght = self.pos - world_mouse
            start = camera.world_pos_to_screen_pos(self.pos)
            end = camera.world_pos_to_screen_pos(self.pos + lenght)
            pygame.draw.line(screen, (35, 168, 242), start, end, 5)
    
    def handle_event(self, event, camera):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # clic gauche
                # Conversion de la position de la souris en coordonnées du monde
                world_mouse = camera.offset + pygame.Vector2(event.pos) / camera.zoom
                if self.rect.collidepoint(world_mouse):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                # Calculer le vecteur de lancement à partir de la position de la souris
                mouse_pos = pygame.Vector2(event.pos)
                world_mouse = camera.offset + mouse_pos / camera.zoom
                self.launch_vector = self.pos - world_mouse
                # Appliquer un facteur de mise à l'échelle pour la vitesse
                self.velocity += self.launch_vector * 0.5
                self.dragging = False
