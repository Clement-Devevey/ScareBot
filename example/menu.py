## Importation des bibliothèques nécessaires
import time, os, sys
import pygame
from pygame.locals import *


clock = pygame.time.Clock()#Permet de régler les FPS (voir ligne 606 : clock.tick(fps))
x_fen = 320
y_fen = 240
fps=60
pygame.display.init()

fenetre = pygame.display.set_mode((x_fen,y_fen))
nbr_choix_menu=2
# On enlève l'affichage de la souris
pygame.mouse.set_visible(False)
fond_vert = pygame.image.load("./Resources/images/fond_vert.png").convert()
curseur_selection = pygame.image.load("./Resources/images/curseur_selection_menu_gameboy.png").convert_alpha()
def affiche_menu(choix):
    """ Affiche le menu et la selection de l'action prochaine à l'aide d'un curseur """
    fenetre.blit(fond_vert, (0,0)) # Affiche de l'interface du menu

    if(choix == 0): # Choix de la position du curseur en fonction du choix
        fenetre.blit(curseur_selection, (65,102))
    elif(choix == 1):
        fenetre.blit(curseur_selection, (65,163))

    pygame.display.flip() # Mis à jour de l'affichage
choix_menu=0
continuer = 1
while continuer:
    affiche_menu(choix_menu)
    clock.tick(fps) # Bloque le jeu à fps FPS
    for event in [pygame.event.wait()]+pygame.event.get():
        if event.type == QUIT:     #Si un de ces événements est de type QUIT
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN: # Si le joueur appuie sur le bouton qui correspond à "bas"
            choix_menu = (choix_menu+1)%nbr_choix_menu # on change la variable qui contient le choix du menu (pour rafficher le bon menu)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP: # Si le joueur appuie sur le bouton qui correspond à "haut"
            choix_menu = (choix_menu-1)%nbr_choix_menu # Mis à jour de la variable qui stocke le choix du joueur

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Si le joueur valide son choix via le bouton qui correspond à espace
            if (choix_menu == 0):
                # pygame.display.set_caption("Blob Runner") # Nom de la fenêtre
                os.system('python3 ./mixerPYbot.py&')
                pygame.quit()
                sys.exit()

            """elif (choix_menu == 1):
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()"""

pygame.quit()
pygame.mixer.quit()
sys.exit()
