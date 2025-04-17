import pygame

from game import Game
from button import ImageButton



pygame.init()

#création de la fenêtre
pygame.display.set_caption("Space mission")
screen = pygame.display.set_mode((1920, 1080))

background = pygame.image.load('assets/UI/background.png')
clock = pygame.time.Clock()
quit_button = ImageButton(1856, 0, "assets/sprites/buttons/button_close.png", scale=1.0)

game = Game(screen)

running = True
while running:
    """
    Boucle principale. 
    Un tour de boucle = un frame du jeu
    à chaque frame, on gère les changements, on efface tout l'écran, on enregistre les changements des éléments, puis on réaffiche tout, avec les modifications
    """
    #partie principale du jeu
    clock.tick(60)
    screen.blit(background, (0, 0)) #vider l'écran

    game.camera.update()
    game.update(screen)



    #mettre à jour les éléments
    game.etoiles.draw(screen, game.camera)
    game.player.draw(screen, game.camera)
    for planet in game.planets:
        planet.draw(screen, game.camera)
    quit_button.draw(screen)



    #mettre à jour l'écran
    pygame.display.flip()

    old_zoom = game.zoom

    # Gestion des événements
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
            if event.button == 1:  # Clic gauche
                if quit_button.is_clicked(event.pos):
                    running = False  # Ferme le jeu si le bouton est cliqué

