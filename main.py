import pygame
from game import Game
from button import ImageButton
from levels import level1, level2, level3

pygame.init()
pygame.font.init()

# Création de la fenêtre
pygame.display.set_caption("Space mission")
screen = pygame.display.set_mode((1920, 1080))

# Chargement des éléments
background = pygame.image.load('assets/UI/background.png')
clock = pygame.time.Clock()

# Polices
rules_font = pygame.font.SysFont('DIN', 18)
level_font = pygame.font.SysFont('DIN', 40)

# États de l'interface
show_menu = True
show_rules = False
show_levels = False  # Nouvel état pour les niveaux

# Boutons
quit_button = ImageButton(1856, 0, "assets/sprites/buttons/button_close.png", width=64, height=64)
play_button = ImageButton(350, 550, "assets/sprites/buttons/button_play_inerte.png",
                         "assets/sprites/buttons/button_play_survol.png", width=280, height=64)
rules_button = ImageButton(360, 800, "assets/sprites/buttons/button_regle_inerte.png",
                         "assets/sprites/buttons/button_regle_survol.png", width=280, height=64)
levels_button = ImageButton(355, 675, "assets/sprites/buttons/button_niveaux_inerte.png",
                          "assets/sprites/buttons/button_niveaux_survol.png", width=280, height=64)
back_button = ImageButton(50, 50, "assets/sprites/buttons/button_back.png", width=50, height=50)

# Boutons pour les niveaux
level1_button = ImageButton(600, 300, "assets/sprites/buttons/button_level1.png",
                           "assets/sprites/buttons/button_level1_hover.png", width=200, height=80)
level2_button = ImageButton(900, 300, "assets/sprites/buttons/button_level2.png",
                           "assets/sprites/buttons/button_level2_hover.png", width=200, height=80)
level3_button = ImageButton(1200, 300, "assets/sprites/buttons/button_level3.png",
                           "assets/sprites/buttons/button_level3_hover.png", width=200, height=80)

# Image en bas à droite
image_bas_droite = pygame.image.load("assets/UI/astronaute_haute_def.PNG")
image_bas_droite = pygame.transform.scale(image_bas_droite, (200, 200))

# Logo
logo = pygame.image.load('assets/sprites/buttons/logo_jeu.png')
logo = pygame.transform.scale(logo, (800, 800))
logo_rect = logo.get_rect(topleft=(150, -150))

game = Game(screen)

running = True

while running:
    game.dt = clock.tick(60) / 1000
    screen.blit(background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if show_menu and not show_rules and not show_levels:
        # Menu principal
        screen.blit(logo, logo_rect)
        play_button.update(mouse_pos)
        rules_button.update(mouse_pos)
        levels_button.update(mouse_pos)
        play_button.draw(screen)
        quit_button.draw(screen)
        rules_button.draw(screen)
        levels_button.draw(screen)
    elif show_rules:
        # Écran des règles
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        rules_rect = pygame.Rect(300, 150, 1320, 780)
        pygame.draw.rect(screen, (50, 50, 80), rules_rect)
        pygame.draw.rect(screen, (100, 100, 150), rules_rect, 5)

        title = pygame.font.SysFont('DIN', 60).render("Règles du Jeu", True, (255, 255, 0))
        screen.blit(title, (rules_rect.centerx - title.get_width() // 2, rules_rect.y + 30))

        rules_text = [
            "Bienvenue dans Derive!",
            "QU'EST-CE QUE DERIVE ?",
            "Derive est un jeu indépendant crée par des étudiants en ingénierie",
            "Nous espérons que vous passerez un très bon moment !",
            "Objectif du jeu: Naviguer dans l'espace et collecter tous les carburants",
            "Avant de rejoindre la station spatiale d'arrivée.",
            "",
            "Contrôles:",
            "- Tirer la souris dans une direction pour lancer le vaisseau dans la direction opposée !",
            "- Clic gauche et bouger la souris pour déplacer la caméra",
            "- Molette de souris pour zoomer/dézoomer",
            "- Espace pour centrer la caméra sur le vaisseau",
            "",
            "CONSEILS",
            "Attention aux planètes (surtout les gazeuses) !",
            "Avoir une souris",
            "Bonne chance dans votre mission spatiale Commandant!",
        ]

        y_offset = 150
        for line in rules_text:
            text_surface = rules_font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (rules_rect.x + 50, rules_rect.y + y_offset))
            y_offset += 40

        back_button.update(mouse_pos)
        back_button.draw(screen)

        image_rect = image_bas_droite.get_rect()
        image_rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)
        screen.blit(image_bas_droite, image_rect)
    elif show_levels:
        # Ecran pour les niveaux
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        levels_rect = pygame.Rect(300, 150, 1320, 780)
        pygame.draw.rect(screen, (50, 50, 80), levels_rect)
        pygame.draw.rect(screen, (100, 100, 150), levels_rect, 5)

        title = pygame.font.SysFont('DIN', 60).render("Sélection du Niveau", True, (255, 255, 0))
        screen.blit(title, (levels_rect.centerx - title.get_width() // 2, levels_rect.y + 30))

        # Boutons des niveaux
        level1_button.update(mouse_pos)
        level2_button.update(mouse_pos)
        level3_button.update(mouse_pos)
        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)

        back_button.update(mouse_pos)
        back_button.draw(screen)

        image_rect = image_bas_droite.get_rect()
        image_rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)
        screen.blit(image_bas_droite, image_rect)
    else:
        # Jeu en cours
        game.camera.update()
        game.update(screen)
        game.etoiles.draw(screen, game.camera)
        game.player.draw(screen, game.camera)
        for planet in game.planets:
            planet.draw(screen, game.camera)
        for collectible in game.collectibles:
            collectible.update()
            collectible.draw(screen, game.camera)
        quit_button.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_SPACE:
                game.camera.anchored = not game.camera.anchored
                if game.camera.anchored:
                    game.camera.recenter_on_player()

        if event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        if event.type == pygame.MOUSEWHEEL:
            zoom_factor = 1.1 if event.y > 0 else 0.9
            game.camera.set_zoom(zoom_factor)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit_button.is_clicked(event.pos):
                    running = False
                elif show_menu and not show_rules and not show_levels:
                    if play_button.is_clicked(event.pos):
                        show_menu = False
                        game.load_level(level1)
                        game.camera.anchored = True
                        game.camera.recenter_on_player()
                        game.camera.update()
                    elif rules_button.is_clicked(event.pos):
                        show_rules = True
                    elif levels_button.is_clicked(event.pos):
                        show_levels = True
                elif show_rules and back_button.is_clicked(event.pos):
                    show_rules = False
                elif show_levels:
                    if back_button.is_clicked(event.pos):
                        show_levels = False
                    elif level1_button.is_clicked(event.pos):
                        show_menu = False
                        show_levels = False
                        game.load_level(level1)
                        game.camera.anchored = True
                        game.camera.recenter_on_player()
                    elif level2_button.is_clicked(event.pos):
                        show_menu = False
                        show_levels = False
                        game.load_level(level2)
                        game.camera.anchored = True
                        game.camera.recenter_on_player()
                    elif level3_button.is_clicked(event.pos):
                        show_menu = False
                        show_levels = False
                        game.load_level(level3)
                        game.camera.anchored = True
                        game.camera.recenter_on_player()

        game.player.handle_event(event, game.camera)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not show_menu:
                world_mouse = game.camera.offset + pygame.Vector2(event.pos) / game.camera.zoom
                if not game.player.rect.collidepoint(world_mouse):
                    game.camera.dragging = True
                    game.camera.anchored = False
                    game.camera.drag_start = pygame.Vector2(event.pos)
                    game.camera.drag_offset_start = game.camera.offset.copy()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                game.camera.dragging = False

pygame.quit()