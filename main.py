import pygame

from game import Game




pygame.init()

#création de la fenêtre
pygame.display.set_caption("Space mission")
screen = pygame.display.set_mode((1920, 1080))

background = pygame.image.load('assets/UI/background.png')

game = Game()

running = True
while running:
    """
    Boucle principale. 
    Un tour de boucle = un frame du jeu
    à chaque frame, on gère les changements, on efface tout l'écran, on enregistre les changements des éléments, puis on réaffiche tout, avec les modifications
    """
    #partie principale du jeu
    game.update()

    #vider l'ecran
    screen.blit(background, (0, 0))

    #mettre à jour les éléments
    game.etoiles.draw(screen)
    screen.blit(game.player.image, game.player.rect)

    #mettre à jour l'écran
    pygame.display.flip()


    #gestion des evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
        #gestion des touches
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False