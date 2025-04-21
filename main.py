import pygame

from game import Game
from button import ImageButton



pygame.init()

#création de la fenêtre
pygame.display.set_caption("Space mission")
screen = pygame.display.set_mode((1920, 1080))

background = pygame.image.load('assets/UI/background.png')
clock = pygame.time.Clock()  # Permet de réguler le nombre de FPS
quit_button = ImageButton(  # Crée un bouton de fermeture en haut à droite
    1856, 0,
    "assets/sprites/buttons/button_close.png",
    width=64, height=64
)

game = Game(screen)

running = True # Contrôle la boucle principale du jeu

logo = pygame.image.load('assets/sprites/buttons/logo_jeu.png')# Ajoute le logo à l'écran d'accueil
logo = pygame.transform.scale(logo, (800, 800))
logo_rect = logo.get_rect(topleft=(150, -150))

play_button = ImageButton( # Crée un bouton de play sur le menu d'accueil
    350, 550,
    "assets/sprites/buttons/button_play_inerte.png",
    "assets/sprites/buttons/button_play_survol.png",
    width=280, height=64
)

show_menu = True

while running:
    """
    Boucle principale. 
    Un tour de boucle = un frame du jeu
    à chaque frame, on gère les changements, on efface tout l'écran, on enregistre les changements des éléments, puis on réaffiche tout, avec les modifications
    """

    clock.tick(60) # Limite les FPS à 60
    screen.blit(background, (0, 0)) # Vide l'écran

    if show_menu:
        # Affichage de l'écran d'accueil
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(logo, logo_rect)
        play_button.update(mouse_pos)
        play_button.draw(screen)
        quit_button.draw(screen)
    else : #Dessine tous les éléments
        game.camera.update()  # Met à jour la position et zoom de la caméra
        game.update(screen)  # Met à jour tous les objets du jeu
        game.etoiles.draw(screen, game.camera)
        game.player.draw(screen, game.camera)
        for planet in game.planets:
            planet.draw(screen, game.camera)
        quit_button.draw(screen)

    pygame.display.flip() # Met à jour l'affichage de l'écran avec toutes les nouvelles images

    old_zoom = game.zoom # Stocke l’ancien zoom

    for event in pygame.event.get():

        if event.type == pygame.QUIT: # Si l’utilisateur ferme la fenêtre
            running = False # Ferme le jeu

        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True # Enregistre qu’une touche est enfoncée
            if event.key == pygame.K_SPACE:
                game.camera.anchored = not game.camera.anchored
                if game.camera.anchored:
                    game.camera.recenter_on_player() # Recentrer immédiatement si ancrée

        if event.type == pygame.KEYUP:  # Une touche est relâchée
            game.pressed[event.key] = False

        if event.type == pygame.MOUSEWHEEL: # Molette de souris
            zoom_factor = 1.1 if event.y > 0 else 0.9 # Zoom in ou zoom out
            game.camera.set_zoom(zoom_factor)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #clique gauche
                if quit_button.is_clicked(event.pos): # Si clic sur le bouton quitter
                    running = False  # Ferme le jeu
                if show_menu and play_button.is_clicked(event.pos):
                    show_menu = False  # Quitte le menu et lance le jeu

