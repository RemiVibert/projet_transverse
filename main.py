import pygame
from game import Game
from button import ImageButton
from base import Base
from player import Player


import ctypes

def warn_message():
    """Ouvre une fenêtre pycharm avec l'image de fond indiquant le problème, qui se ferme quand on clique."""
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware() # Ajuste la DPI pour l'écran de l'utilisateur
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    pygame.init()
    pygame.display.set_caption("Résolution insuffisante")
    screen = pygame.display.set_mode((screen_width, screen_height))

    background = pygame.image.load('assets/UI/screen_res_background.PNG').convert()
    background = pygame.transform.scale(background, (screen_width, screen_height)) # Redimensionner le fond pour couvrir tout l'écran

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.blit(background, (0, 0))
        pygame.display.flip()

    pygame.quit()

def start():
    n = 0
    SCREEN_SIZE = (1920, 1080) # Taille de l'écran du jeu


    pygame.init()
    pygame.font.init()  # Initialisation du module de polices

    # Création de la fenêtre
    pygame.display.set_caption("Space mission")
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Chargement des éléments
    background = pygame.image.load('assets/UI/background.png')
    clock = pygame.time.Clock()


    # Images du fond de fin de niveau
    end_background_victory = pygame.image.load("assets/level_end_screen/image_fin_niveau.png").convert()
    end_background_game_over = pygame.image.load("assets/level_end_screen/game_over_screen.png").convert()
    dead_crash_img = pygame.image.load("assets/level_end_screen/dead_crash.png").convert_alpha()
    dead_no_fuel_img = pygame.image.load("assets/level_end_screen/dead_no_fuel.png").convert_alpha()
    dead_lost_img = pygame.image.load("assets/level_end_screen/dead_lost.png").convert_alpha()

    background_screen_res = pygame.image.load("assets/UI/screen_res_background.PNG").convert() #Fond pour avertir d'une mauvaise résolution

    game = Game(screen)
    player = game.player

    rules_font = pygame.font.SysFont('DIN', 18) # Police pour les règles

    # États de l'interface
    show_menu = True
    show_rules = False
    show_end_screen = False
    show_levels = False

    # Boutons de menus
    quit_button = ImageButton(1856, 0, "assets/sprites/buttons/button_close.png", width=64, height=64)

    play_button = ImageButton(350, 550, "assets/sprites/buttons/button_play_inerte.png",
                            "assets/sprites/buttons/button_play_survol.png", width=280, height=64)

    rules_button = ImageButton(360, 800, "assets/sprites/buttons/button_regle_inerte.png",
                            "assets/sprites/buttons/button_regle_survol.png", width=280, height=64)

    levels_button = ImageButton(355, 675, "assets/sprites/buttons/button_niveaux_inerte.png",
                                "assets/sprites/buttons/button_niveaux_survol.png", width=280, height=64)

    back_button = ImageButton(50, 50, "assets/sprites/buttons/button_back.png", width=50, height=50)

    main_menu_button_game_over = ImageButton(855, 640, "assets/sprites/buttons/button_return_main_menu.png", width=70, height=70)

    play_again_button_game_over = ImageButton(995, 640, "assets/sprites/buttons/button_play_again.png", width=70, height=70)

    main_menu_button_victory = ImageButton(825, 680, "assets/sprites/buttons/button_return_main_menu.png", width=70, height=70)

    play_again_button_victory = ImageButton(945, 680, "assets/sprites/buttons/button_play_again.png", width=70, height=70)

    next_level_button = ImageButton(1065, 680, "assets/sprites/buttons/button_next_level.png", width=70, height=70)

    ok_button = ImageButton(890, 720, "assets/sprites/buttons/button_ok.PNG", width=140, height=70)

    # Boutons pour les niveaux
    level1_button = ImageButton(500, 300, "assets/sprites/buttons/button_level1.png",
                            "assets/sprites/buttons/button_level1_hover.png", width=80, height=80)
    level2_button = ImageButton(700, 300, "assets/sprites/buttons/button_level2.png",
                            "assets/sprites/buttons/button_level2_hover.png", width=80, height=80)
    level3_button = ImageButton(900, 300, "assets/sprites/buttons/button_level3.png",
                            "assets/sprites/buttons/button_level3_hover.png", width=80, height=80)
    level4_button = ImageButton(1100, 300, "assets/sprites/buttons/button_level4.png",
                            "assets/sprites/buttons/button_level4_hover.png", width=80, height=80)
    level5_button = ImageButton(1300, 300, "assets/sprites/buttons/button_level5.png",
                            "assets/sprites/buttons/button_level5_hover.png", width=80, height=80)
    level6_button = ImageButton(600, 450, "assets/sprites/buttons/button_level6.png",
                            "assets/sprites/buttons/button_level6_hover.png", width=80, height=80)
    level7_button = ImageButton(800, 450, "assets/sprites/buttons/button_level7.png",
                            "assets/sprites/buttons/button_level7_hover.png", width=80, height=80)
    level8_button = ImageButton(1000, 450, "assets/sprites/buttons/button_level8.png",
                            "assets/sprites/buttons/button_level8_hover.png", width=80, height=80)
    level9_button = ImageButton(1200, 450, "assets/sprites/buttons/button_level9.png",
                            "assets/sprites/buttons/button_level9_hover.png", width=80, height=80)
    level10_button = ImageButton(1400, 450, "assets/sprites/buttons/button_level10.png",
                            "assets/sprites/buttons/button_level10_hover.png", width=80, height=80)
    level11_button = ImageButton(500, 600, "assets/sprites/buttons/button_level11.png",
                            "assets/sprites/buttons/button_level11_hover.png", width=80, height=80)
    level12_button = ImageButton(700, 600, "assets/sprites/buttons/button_level12.png",
                            "assets/sprites/buttons/button_level12_hover.png", width=80, height=80)
    level13_button = ImageButton(900, 600, "assets/sprites/buttons/button_level13.png",
                            "assets/sprites/buttons/button_level13_hover.png", width=80, height=80)
    level14_button = ImageButton(1100, 600, "assets/sprites/buttons/button_level14.png",
                            "assets/sprites/buttons/button_level14_hover.png", width=80, height=80)
    level15_button = ImageButton(1300, 600, "assets/sprites/buttons/button_level15.png",
                            "assets/sprites/buttons/button_level15_hover.png", width=80, height=80)
    level16_button = ImageButton(600, 750, "assets/sprites/buttons/button_level16.png",
                            "assets/sprites/buttons/button_level16_hover.png", width=80, height=80)
    level17_button = ImageButton(800, 750, "assets/sprites/buttons/button_level17.png",
                            "assets/sprites/buttons/button_level17_hover.png", width=80, height=80)
    level18_button = ImageButton(1000, 750, "assets/sprites/buttons/button_level18.png",
                            "assets/sprites/buttons/button_level18_hover.png", width=80, height=80)
    level19_button = ImageButton(1200, 750, "assets/sprites/buttons/button_level19.png",
                            "assets/sprites/buttons/button_level19_hover.png", width=80, height=80)
    level20_button = ImageButton(1400, 750, "assets/sprites/buttons/button_level20.png",
                            "assets/sprites/buttons/button_level20_hover.png", width=80, height=80)


    # Image en bas à droite du menu des règles
    image_bas_droite = pygame.image.load("assets/UI/astronaute_haute_def.PNG")
    image_bas_droite = pygame.transform.scale(image_bas_droite, (250, 250))

    # Logo
    logo = pygame.image.load('assets/sprites/buttons/logo_jeu.png')
    logo = pygame.transform.scale(logo, (800, 800))
    logo_rect = logo.get_rect(topleft=(150, -150))

    game = Game(screen)

    running = True

    # Initialisation des musiques
    intro_musique = True
    pygame.mixer.music.load("assets/audio/Happy Hills - Pianomations_intro.mp3")
    pygame.mixer.music.set_volume(0.5)  # Ajuster le volume (0.0 à 1.0)
    pygame.mixer.music.play()  # Jouer la musique d'intro une seule fois

    # Configurer un événement pour détecter la fin de la musique d'intro
    MUSIC_END_EVENT = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

    # Musique de loop
    loop_music_path = "assets/audio/Happy Hills - Pianomations_loop.mp3"
    image_planete = pygame.image.load("assets/sprites/planetes/grande-rocheuse.png")
    while running:
        game.dt = clock.tick(60) / 1000
        mouse_pos = pygame.mouse.get_pos()

        if show_menu and not show_rules:
            # Menu principal
            screen.blit(background, (0, 0))  # Affiche le fond du menu
            screen.blit(image_planete, (1000, -128)) 
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

                star_image = pygame.image.load("assets/level_end_screen/star_end_level.png").convert_alpha()
                star_size = 200
                num_stars = game.calculate_stars()
                star_positions = [
                    (700, 200),  # Position de la 1ère étoile
                    (900, 200),  # Position de la 2ème étoile
                    (1100, 200)  # Position de la 3ème étoile
                ]

                for i in range(num_stars):
                    if i < len(star_positions):
                        x, y = star_positions[i]
                        star_scaled = pygame.transform.scale(star_image, (star_size, star_size))
                        screen.blit(star_scaled, (x, y))
            else :
                screen.blit(end_background_game_over, (0, 0))
                if hasattr(game, 'death_overlay') and game.death_overlay:
                    screen.blit(game.death_overlay, (710, 300))
                main_menu_button_game_over.draw(screen)
                play_again_button_game_over.draw(screen)
                quit_button.draw(screen)


        elif show_levels:
            # Ecran pour les niveaux
            overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, ))
            screen.blit(overlay, (0, 0))

            levels_rect = pygame.Rect(300, 150, 1320, 780)

            title = pygame.font.SysFont('DIN', 60).render("Choisissez votre niveau : ", True, (255, 255, 255))
            screen.blit(title, (levels_rect.centerx - title.get_width() // 2, levels_rect.y + 30))

            # Boutons des niveaux
            level1_button.update(mouse_pos)
            level2_button.update(mouse_pos)
            level3_button.update(mouse_pos)
            level4_button.update(mouse_pos)
            level5_button.update(mouse_pos)
            level6_button.update(mouse_pos)
            level7_button.update(mouse_pos)
            level8_button.update(mouse_pos)
            level9_button.update(mouse_pos)
            level10_button.update(mouse_pos)
            level11_button.update(mouse_pos)
            level12_button.update(mouse_pos)
            level13_button.update(mouse_pos)
            level14_button.update(mouse_pos)
            level15_button.update(mouse_pos)
            level16_button.update(mouse_pos)
            level17_button.update(mouse_pos)
            level18_button.update(mouse_pos)
            level19_button.update(mouse_pos)
            level20_button.update(mouse_pos)

            level1_button.draw(screen)
            level2_button.draw(screen)
            level3_button.draw(screen)
            level4_button.draw(screen)
            level5_button.draw(screen)
            level6_button.draw(screen)
            level7_button.draw(screen)
            level8_button.draw(screen)
            level9_button.draw(screen)
            level10_button.draw(screen)
            level11_button.draw(screen)
            level12_button.draw(screen)
            level13_button.draw(screen)
            level14_button.draw(screen)
            level15_button.draw(screen)
            level16_button.draw(screen)
            level17_button.draw(screen)
            level18_button.draw(screen)
            level19_button.draw(screen)
            level20_button.draw(screen)


            back_button.update(mouse_pos)
            back_button.draw(screen)

            image_rect = image_bas_droite.get_rect()
            image_rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)
        elif show_rules:
            # Écran des règles
            overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            rules_rect = pygame.Rect(300, 150, 1320, 780)

            title = pygame.font.SysFont('DIN', 60).render("Règles du Jeu", True, (255, 255, 255))
            screen.blit(title, (rules_rect.centerx - title.get_width() // 2, rules_rect.y + 30))

            # Texte des règles
            rules_text = [
                "HISTOIRE",
                "Vous êtes le Capitaine Meko, traversant l'espace pour rejoindre la station spatiale. ",
                "En cours de route, vous rencontrez des astronautes qui ont l'air d'avoir besoin d'aide... !",
                "L'objectif du jeu est de naviguer dans l'espace et de rejoindre la station spatiale d'arrivée tout en évitant de tomber à court de carburant.",
                "",
                "Contrôles:",
                "- Tirer la souris dans une direction pour lancer le vaisseau dans la direction opposée !",
                "- Molette de souris pour zoomer/dézoomer",
                "- Espace pour centrer ou décentrer la caméra sur le vaisseau",
                "- Une fois décentrée, bouger la souris pour déplacer la caméra",
                "",
                "CONSEILS",
                "Attention aux planètes (surtout les gazeuses) !",
                "Ramassez les astronautes pour obtenir des étoiles !",
                "N'oubliez pas de récupérer du carburant !",
                "Bonne chance dans votre mission spatiale Commandant !",
            ]
            y_offset = 150
            rules_font = pygame.font.SysFont('DIN', 27)
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
            game.check_victory()
            game.etoiles.draw(screen, game.camera)
            for planet in game.planets:
                planet.draw(screen, game.camera)
            for collectible in game.collectibles:
                collectible.update()
                collectible.draw(screen, game.camera)
            for fuel in game.fuels:
                fuel.draw(screen, game.camera)
            game.player.draw(screen, game.camera)
            game.base.draw(screen, game.camera) # type: ignore
            quit_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            # Vérifier si l'événement de fin de musique est déclenché
            if event.type == MUSIC_END_EVENT:
                if intro_musique:
                    intro_musique = False
                    pygame.mixer.music.load(loop_music_path)
                    pygame.mixer.music.play(-1)  # Jouer la musique de loop en boucle infinie

            if event.type == pygame.QUIT:
                running = False # Arrête la boucle de jeu si la fenêtre est fermée

            if event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_SPACE:
                    game.camera.anchored = not game.camera.anchored # Inverse l'ancrage de la caméra
                    if game.camera.anchored:
                        game.camera.recenter_on_player() # Recentre la caméra sur le joueur

            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

            if event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.1 if event.y > 0 else 0.9 # Détermine le facteur de zoom
                game.camera.set_zoom(zoom_factor)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                world_mouse = game.camera.offset + pygame.Vector2(event.pos) / game.camera.zoom
                if not game.player.rect.collidepoint(world_mouse):  # Si la souris ne touche pas le joueur
                    game.camera.dragging = True
                    game.camera.drag_start = pygame.Vector2(event.pos) # Sauvegarde la position de départ du drag
                    game.camera.drag_offset_start = game.camera.offset.copy() # Sauvegarde la position de départ de l'offset de la caméra
                if event.button == 1:
                    play_button_sound = False # Variable pour gérer le son des boutons
                    if quit_button.is_clicked(event.pos):
                        running = False
                    if show_menu and not show_rules:
                        if play_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level()
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif rules_button.is_clicked(event.pos):
                            play_button_sound = True
                            show_rules = True
                        elif levels_button.is_clicked(event.pos):
                            play_button_sound = True
                            show_levels = True
                            show_menu = False

                    if show_rules and back_button.is_clicked(event.pos):
                        play_button_sound = True
                        show_rules = False
                        show_menu = True

                    if show_levels:
                        if back_button.is_clicked(event.pos):
                            play_button_sound = True
                            show_levels = False
                            show_menu = True
                        # Gestion des clics sur les différents boutons de niveaux
                        elif level1_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(0)
                            n = 0
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level2_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(1)
                            n = 1
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level3_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(2)
                            n = 2
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level4_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(3)
                            n = 3
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level5_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(4)
                            n = 4
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level6_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(5)
                            n = 5
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level7_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(6)
                            n = 6
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level8_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(7)
                            n = 7
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level9_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(8)
                            n = 8
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level10_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(9)
                            n = 9
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level11_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(10)
                            n = 10
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level12_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(11)
                            n = 11
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level13_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(12)
                            n = 12
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level14_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(13)
                            n = 13
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level15_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(14)
                            n = 14
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level16_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(15)
                            n = 15
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level17_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(16)
                            n = 16
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level18_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(17)
                            n = 17
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level19_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(18)
                            n = 18
                            game.camera.anchored = True
                            game.camera.recenter_on_player()
                        elif level20_button.is_clicked(event.pos):
                            show_menu = False
                            show_levels = False
                            game.load_level(19)
                            n = 19
                            game.camera.anchored = True
                            game.camera.recenter_on_player()

                    if game.end_screen_active:
                        if game.victoire:
                            if main_menu_button_victory.is_clicked(event.pos):
                                play_button_sound = True
                                game.end_screen_active = False
                                show_menu = True
                            elif play_again_button_victory.is_clicked(event.pos):
                                game.end_screen_active = False
                                game.load_level(n)

                            elif next_level_button.is_clicked(event.pos):
                                game.end_screen_active = False
                                n += 1
                                if n != 20:
                                    game.load_level(n)
                                else:
                                    n = 0
                                    game.load_level(n)

                        else:  # Si le joueur a perdu
                            if main_menu_button_game_over.is_clicked(event.pos):
                                play_button_sound = True
                                game.end_screen_active = False
                                show_menu = True
                            elif play_again_button_game_over.is_clicked(event.pos):
                                game.end_screen_active = False
                                game.load_level(n)

                    if play_button_sound:
                        pygame.mixer.Sound("assets/audio/clic.mp3").play() # Joue le son du clic

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        game.camera.dragging = False # Arrête le drag de la caméra
            game.player.handle_event(event, game.camera)

# Détection de la taille de l'écran physique en tenant compte de la mise à l'échelle Windows
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()  # Prend en compte la mise à l'échelle Windows
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if screen_width < 1920 or screen_height < 1080:
    print(f"\033[1;31mLa fenêtre de jeu n'a pas la bonne taille\033[0m")
    warn_message()
else:
    start()
    pygame.quit()