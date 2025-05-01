import pygame
from game import Game
from button import ImageButton
from levels import level1
from base import Base
from player import Player


SCREEN_SIZE = (1920, 1080)
# SCREEN_SIZE = (960, 540)  # Pour le test sur l'ordinateur portable


pygame.init()
pygame.font.init()  # Initialisation du module de polices

# Création de la fenêtre
pygame.display.set_caption("Space mission")
screen = pygame.display.set_mode(SCREEN_SIZE)

# Chargement des éléments
background = pygame.image.load('assets/UI/background.png')
clock = pygame.time.Clock()
base_img = pygame.image.load("assets/sprites/base/base.png").convert_alpha()
base = Base(2000, 2000, base_img)
end_background_victory = pygame.image.load("assets/level_end_screen/image_fin_niveau.PNG").convert()
end_background_victory = pygame.image.load("assets/level_end_screen/game_over_screen.png").convert()
player = Player(Game)


# Police pour les règles
rules_font = pygame.font.SysFont('DIN', 18)

# États de l'interface
show_menu = True
show_rules = False
show_end_screen = False

# Boutons
quit_button = ImageButton(1856, 0, "assets/sprites/buttons/button_close.png", width=64, height=64)

play_button = ImageButton(350, 550, "assets/sprites/buttons/button_play_inerte.png",
                          "assets/sprites/buttons/button_play_survol.png", width=280, height=64)

rules_button = ImageButton(360, 800, "assets/sprites/buttons/button_regle_inerte.png",
                           "assets/sprites/buttons/button_regle_survol.png", width=280, height=64)

levels_button = ImageButton(355, 675, "assets/sprites/buttons/button_niveaux_inerte.png",
                            "assets/sprites/buttons/button_niveaux_survol.png", width=280, height=64)

back_button = ImageButton(50, 50, "assets/sprites/buttons/button_back.png", width=50, height=50)

main_menu_button_game_over = ImageButton(855, 540, "assets/sprites/buttons/button_return_main_menu.png", width=70, height=70)

play_again_button_game_over = ImageButton(995, 540, "assets/sprites/buttons/button_play_again.png", width=70, height=70)

main_menu_button_victory = ImageButton(805, 540, "assets/sprites/buttons/button_return_main_menu.png", width=70, height=70)

play_again_button_victory = ImageButton(925, 540, "assets/sprites/buttons/button_play_again.png", width=70, height=70)

next_level_button = ImageButton(1115, 540, "assets/sprites/buttons/button_next_level.png", width=70, height=70)

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
    mouse_pos = pygame.mouse.get_pos()

    if show_menu and not show_rules:
        # Menu principal
        screen.blit(background, (0, 0))  # Affiche le fond du menu
        screen.blit(logo, logo_rect)
        play_button.update(mouse_pos)
        rules_button.update(mouse_pos)
        levels_button.update(mouse_pos)
        play_button.draw(screen)
        quit_button.draw(screen)
        rules_button.draw(screen)
        levels_button.draw(screen)

    elif game.end_screen_active :
        # Ecran de fin de niveau
        if game.victoire:
            screen.blit(end_background_victory, (0, 0))
            main_menu_button_victory.draw(screen)
            play_again_button_victory.draw(screen)
            next_level_button.draw(screen)
            quit_button.draw(screen)
        else :
            screen.blit(end_background_victory, (0, 0))
            main_menu_button_game_over.draw(screen)
            play_again_button_game_over.draw(screen)
            quit_button.draw(screen)


    elif show_rules:
        # Écran des règles
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        rules_rect = pygame.Rect(300, 150, 1320, 780)
        pygame.draw.rect(screen, (50, 50, 80), rules_rect)
        pygame.draw.rect(screen, (100, 100, 150), rules_rect, 5)

        title = pygame.font.SysFont('DIN', 60).render("Règles du Jeu", True, (255, 255, 0))
        screen.blit(title, (rules_rect.centerx - title.get_width() // 2, rules_rect.y + 30))

        # Texte des règles
        rules_text = [
            "Bienvenue dans Derive!",
            "QU'EST-CE QUE DERIVE ?",
            "Derive est un jeu indépendant créé par des étudiants en ingénierie",
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

    else:
        # Jeu en cours - Fond du jeu
        screen.fill((0, 0, 0))  # Efface l'écran pour afficher la scène du jeu
        game.camera.update()
        game.update(screen)
        game.etoiles.draw(screen, game.camera)
        for planet in game.planets:
            planet.draw(screen, game.camera)
        for collectible in game.collectibles:
            collectible.update()
            collectible.draw(screen, game.camera)
        game.player.draw(screen, game.camera)
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
                elif show_menu and not show_rules:
                    if play_button.is_clicked(event.pos):
                        show_menu = False
                        game.load_level(level1)
                        game.camera.anchored = True
                        game.camera.recenter_on_player()
                        game.camera.update()
                    elif rules_button.is_clicked(event.pos):
                        show_rules = True
                elif show_rules and back_button.is_clicked(event.pos):
                    show_rules = False
                elif game.end_screen_active and main_menu_button_game_over.is_clicked(event.pos):
                    show_menu = True
                    game.end_screen_active = False
                elif game.end_screen_active and main_menu_button_victory.is_clicked(event.pos):
                    show_menu = True
                    game.end_screen_active = False
                elif game.end_screen_active and play_again_button_game_over.is_clicked(event.pos):
                    game.load_level(level1)
                elif game.end_screen_active and play_again_button_victory.is_clicked(event.pos):
                    game.load_level(level1)

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