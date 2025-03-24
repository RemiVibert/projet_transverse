import pygame

from game import Game




pygame.init()

#création de la fenêtre
pygame.display.set_caption("Space mission")
screen = pygame.display.set_mode((1920, 1080))

background = pygame.image.load('assets/UI/background.png')
clock = pygame.time.Clock()


game = Game()

running = True
while running:
    """
    Boucle principale. 
    Un tour de boucle = un frame du jeu
    à chaque frame, on gère les changements, on efface tout l'écran, on enregistre les changements des éléments, puis on réaffiche tout, avec les modifications
    """
    #partie principale du jeu
    game.update(screen)

    #vider l'ecran
    screen.blit(background, (0, 0))

    #mettre à jour les éléments
    game.etoiles.draw(screen, game.camera)
    game.player.draw(screen, game.camera)
#    screen.blit(game.player.image, game.player.rect)

    #mettre à jour l'écran
    pygame.display.flip()


    
    old_zoom = game.zoom
    #gestion des evenements
    # for event in pygame.event.get():
        
        
    #     #gestion des touches
    #     if event.type == pygame.KEYDOWN:
    #         game.pressed[event.key] = True
        
    #     elif event.type == pygame.KEYUP:
    #         game.pressed[event.key] = False

    #     elif event.type == pygame.MOUSEWHEEL:
    #         if event.y > 0:  # Molette vers le haut : zoom avant
    #             game.zoom = min(game.zoom_max, game.zoom_speed)
    #         elif event.y < 0:  # Molette vers le bas : zoom arrière
    #             game.zoom = max(game.zoom_speed, game.zoom_min)
    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     cam_x = mouse_x - (mouse_x - game.cam_x) * (game.zoom / old_zoom)
    #     cam_y = mouse_y - (mouse_y - game.cam_y) * (game.zoom / old_zoom)
