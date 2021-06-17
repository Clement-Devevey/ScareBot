## Importation des bibliothèques nécessaires
import pygame, time, random, os, sys
from pygame.locals import *
from math import ceil,log10
from gpiozero import LED, Button

## DEFINE
def_button = 0 # 0 : button don't work, 1 : button work
## Variables
continuer = 1
vollvl = 50 #Niveau initial du volume
vol=0.8519443031609923
fps = 60
## Variables globales pour la vitesse
jspeed = -18*(60/fps)  #Vitesse de saut
start_speed = 10*(60/fps) #Vitesse de défilement de départ
acc_speed = 0.005*(60/fps) #Accélération de la vitesse de défilement
gravity = 1.2*(60/fps)**2   #Force de gravité

# Configuration drivers
os.environ['SDL_VIDEODRIVER'] = 'directfb'
os.environ["SDL_FBDEV"] = "/dev/fb0"                          
os.environ["SDL_NOMOUSE"] = "1"
os.environ['SDL_AUDIODRIVER'] = 'alsa'

## Initialisation de la bibliothèque Pygame
pygame.init()
pygame.mixer.init()
theme = pygame.mixer.Sound("./Resources/musiques/8bit.wav")
theme_canal=theme.play(-1) # Joue la musique principale en boucle
theme_canal.set_volume(vol) # set the volume, from 0.0 to 1.0 where higher is louder.
sound_jump = pygame.mixer.Sound("./Resources/musiques/jump.wav")
sound_select = pygame.mixer.Sound("./Resources/musiques/select.wav")
sound_validate = pygame.mixer.Sound("./Resources/musiques/validate.wav")
sound_game_over = pygame.mixer.Sound("./Resources/musiques/gameover.wav")


clock = pygame.time.Clock()#Permet de régler les FPS (voir ligne 606 : clock.tick(fps))
nbr_choix_menu = 2 # les deux choix du menu sont Play ou Quit


## Création de la fenêtre (en pixels)
x_fen = 320
y_fen = 240
fenetre = pygame.display.set_mode((x_fen,y_fen))

## On enlève l'affichage de la souris
pygame.mouse.set_visible(False)

## Chargement des images (Si image avec fond transparent, utiliser .convert_alpha)
fond_vert = pygame.image.load("./Resources/images/fond_vert.png").convert()
menu_fond = pygame.image.load("./Resources/images/menu.png").convert_alpha()
curseur_selection = pygame.image.load("./Resources/images/curseur_selection_menu_gameboy.png").convert_alpha()
sol1 = pygame.image.load("./Resources/images/sol 1.png").convert_alpha()
sol2 = pygame.image.load("./Resources/images/sol 2.png").convert_alpha()
sol3 = pygame.image.load("./Resources/images/sol 3.png").convert_alpha()
sol4 = pygame.image.load("./Resources/images/sol 4.png").convert_alpha()
blob_dead = pygame.image.load("./Resources/images/blob dead.png").convert_alpha()
game_over_texte = pygame.image.load("./Resources/images/game over gameboy.png").convert_alpha()
cloud1 = pygame.image.load("./Resources/images/cloud 1.png").convert_alpha()
cloud2 = pygame.image.load("./Resources/images/cloud 2.png").convert_alpha()
cloud3 = pygame.image.load("./Resources/images/cloud 3.png").convert_alpha()
img_volume = pygame.image.load("./Resources/images/volume.png").convert_alpha()


## Initialisation des Boutons et pins

# Le principe est le suivant : 
# 1) On crée des fonctions
# Chacune de ces fonctions ajoute un event dans la liste des event. De cette façon, on garde la même manière de coder que si on utilisait les touches du clavier.
if(def_button == 1):
    def up_press():
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    def up_release():
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
    def down_press():
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
    def down_release():
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))
    def a_press():
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    def a_release():
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE))
    def b_press():
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    def b_release():
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_ESCAPE))
    def left_press():
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
    def left_release():
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT))
    def right_press():
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
    def right_release():
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))

    # 2) On affecte chaque bouton au bon pin GPIO (voir la documentation de la PI ZERO (pinout PI ZERO) : https://pi4j.com/1.2/pins/model-zerow-rev1.html
    up=Button(16, False, None, 0.075, 1, False, None)
    right=Button(26, False, None, 0.075, 1, False, None)
    down=Button(6, False, None, 0.075, 1, False, None)
    left=Button(5, False, None, 0.075, 1, False, None)
    b=Button(27, False, None, 0.075, 1, False, None)
    a=Button(17, False, None, 0.075, 1, False, None)

    # 3) On affecte à chaque état du bouton (pressé ou relaché) une fonction. Celle-ci sera appelé n'importe quand via interruptions.
    up.when_pressed = up_press
    up.when_released = up_release
    right.when_pressed = right_press
    right.when_released = right_release
    down.when_pressed = down_press
    down.when_released = down_release
    left.when_pressed = left_press
    left.when_released = left_release
    a.when_pressed = a_press
    a.when_released = a_release
    b.when_pressed = b_press
    b.when_released = b_release

class Blob(pygame.sprite.Sprite): # Classe du blob "debout" 
    def __init__(self):
        super().__init__(all_sprite) # Associe le sprite au groupe all_sprite
        self.image = pygame.image.load("./Resources/images/blob_base.png").convert_alpha() # Image du blob
        self.mask = pygame.mask.from_surface(self.image) # Création du mask pour les collisions
        self.rect = self.image.get_rect()
        self.blob_x = 10 # Coordonnée x par défaut du blob
        self.blob_y = 180 # Coordonnée y par défaut du blob
        self.rect.x += self.blob_x # on place le rectangle au bon endroit
        self.rect.y += self.blob_y # on place le rectangle au bon endroit

    def update(self):
        # Permet de mettre à jour les coordonnées du rectangle pour les collisions.
        self.rect.x = self.blob_x
        self.rect.y = self.blob_y


class Blob_crouch(pygame.sprite.Sprite): # Classe du blob "accroupi" 
    def __init__(self):
        super().__init__(all_sprite)  # Associe le sprite au groupe all_sprite
        self.image = pygame.image.load("./Resources/images/blob crouch.png").convert_alpha() # Image du blob accroupi
        self.mask = pygame.mask.from_surface(self.image) # Création du mask pour les collisions
        self.rect = self.image.get_rect() # Création du rectangle pour les collisions
        self.x = 0  #Initialisation de sa coordonnée x
        self.y = 0 #Initialisation de sa coordonnée y

    def update(self):
        # Permet de mettre à jour les coordonnées du rectangle pour les collisions.
        self.rect.x = self.x
        self.rect.y = self.y


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprite) # Associe le sprite au groupe all_sprite
        self.large = pygame.image.load("./Resources/images/large object.png").convert_alpha() #Chargement image large object
        self.mask_large = pygame.mask.from_surface(self.large)
        self.small = pygame.image.load("./Resources/images/small object.png").convert_alpha()  #Chargement image small object
        self.mask_small = pygame.mask.from_surface(self.small)
        self.fantome = pygame.image.load("./Resources/images/fantome gameboy.png").convert_alpha() #Chargement image fantome
        self.mask_fantome = pygame.mask.from_surface(self.fantome)
        self.mask = pygame.mask.from_surface(self.small) # initialisation à un petit obstacle
        self.rect =  self.small.get_rect() # Création du rectangle pour les collisions
        self.x = random.randrange(x_fen+200, 2*x_fen, 2) #on initialise la position horizontale de l'objet aléatoirement (entre x_fen +200 et 2*x_fen)
        self.y = 197 # La coordonnée y est de 197.
        self.type = 1 # Initialisation de l'obstacle à un petit obstacle
        # 0: large , 1: small, 2 : fantome
        

    def update(self):
        """ Met à jour les coordonnées du rectangle puis ajoute l'affichage de l'obstacle sur la fenêtre 
            (/!\ tant qu'on n'a pas appelé fenetre.display(), rien ne s'affiche) """
        if (self.type == 0):
            self.rect.x = self.x
            self.rect.y = self.y
            fenetre.blit(self.large, (self.x, self.y))
        elif (self.type == 1):
            self.rect.x = self.x
            self.rect.y = self.y
            fenetre.blit(self.small, (self.x, self.y))
        elif (self.type == 2):
            self.rect.x = self.x
            self.rect.y = self.y
            fenetre.blit(self.fantome, (self.x, self.y))

    def change_mask(self):
        """ Met à jour le mask et le rectangle, quand l'obstacle sort du cadre de la fenêtre de jeu. 
            (Car quand il sort, on prend un entier random pour changer le type de l'obstacle) """                                            
        if (self.type == 0):
            self.mask = self.mask_large
            self.rect =  self.large.get_rect()
        elif (self.type == 1):
            self.mask = self.mask_small
            self.rect = self.small.get_rect()
        elif (self.type == 2):
            self.mask = self.mask_fantome
            self.rect =  self.fantome.get_rect()
                                

# ## Icon de la fenêtre et nom de la fenêtre
# Permet d'afficher une icone et un titre sur la fenetre, inutile dans notre cas car full screen                                                                                  
# pygame.display.set_icon(blob.image)
# pygame.display.set_caption("Menu de la ScareBot")


## Chargement de la police pour affichage du score
font = pygame.font.Font(r"./Resources/images/pixelmix_bold.ttf", 12)


def affiche_menu(choix,self):
    """ Affiche le menu et la selection de l'action prochaine à l'aide d'un curseur """
    fenetre.blit(fond_vert, (0,0)) # Affichage du fond vert
    fenetre.blit(menu_fond, (0,0)) # Affiche de l'interface du menu
    if(choix == 0): # Choix de la position du curseur en fonction du choix 
        fenetre.blit(curseur_selection, (65,102))      
    elif(choix == 1):
        fenetre.blit(curseur_selection, (65,163))

    texte = font.render('High score: {0}'.format(self.high_score), False, (48,98,48))  # "text", antialias, color
    fenetre.blit(texte, (75, 225))
    pygame.display.flip()
    if self.displayvolume>0 :
        # Affichage de la barre de volume
        fenetre.blit(img_volume, (49,50))
        pygame.draw.rect(fenetre, [15,56, 15], [63, 52, int(1.92*self.vollvl), 10], 0)
        self.displayvolume -=1                
    pygame.display.flip() # Mis à jour de l'affichage 

## Fonction qui clean l'ancien affichage (en affichant le fond vert) :
def clean_affichage(screen):
    """ Nettoyage de l'affichage """
    fenetre.blit(fond_vert, (0,0))
    pygame.display.flip()




## Classe pour gérer les scènes : ici, on a la scènes du menu et celle du jeu
class GameState():
    def __init__(self):
        # Chargement des sounds effects :
        self.sound_jump = sound_jump
        self.sound_select = sound_select
        self.sound_validate = sound_validate
        self.sound_game_over = sound_game_over
        self.canal_sound = pygame.mixer.find_channel()
        
        self.vollvl = vollvl # Gère le volume
        self.state = 'menu' # état par défaut : menu
        self.displayvolume = 0 # Variable qui dit si il faut afficher le rectangle du volume ou pas
        self.choix_menu = 0 # Choix du menu (0 pour jouer et 1 pour quitter). Permet de savoir sur quel choix est l'utilisateur pour afficher le curseur au bon endroit et savoir ce qu'il souhaite faire quand il appuye sur entrée
        self.clean = 0 # Permet de savoir si on passe de l'état menu -> jeu  et jeu -> menu pour faire des modifications UNIQUEMENT lors de la première itération
        self.speed = start_speed # fixe le speed du jeu
        self.score=0 # Initialisation du score à 0 (ne trichez pas svp)
        self.alive = True # Etat du blob (vivant ou mort)
        self.stopjump = False # permet de savoir si l'utilisateur veut arrêter de sauter (il appuye sur saut et relâche avant d'avoir atteint la hateur max du saut)
        self.jump = False # Permet de savoir si on est en train de sauter (pour éviter de spam le saut)
        self.fall = False # Permet de savoir si on est en chute libre (après avoir atteint le saut max, ou si l'utilisateur arrête de saut, on passe en chut libre)
        self.crouch = False # False : le blob n'est pas accroupi // True : le blob est accroupi
        self.jspeed= jspeed #Prends la valeur + ou - jspeed. Utiliser lors du saut, elle permet d'avoir un saut avec une vitesse non linéaire
        self.gravity = gravity # Gravité, aussi utilisé pour avoir un saut avec une vitesse non linéaire (surtout pour la chute)
        self.tab_pos_nuage = [[400,random.randrange(24, 178, 11)], [700,random.randrange(24, 178, 11)],[1000,random.randrange(24, 178, 11)]] # Tableau qui contient la position de chaque nuage. On utilise 3 nuages au maximum.Leur coordonnée y est prise aléatoirement.
        self.tab_type_nuage = [1, 2, 3] # Autre tableau qui définit le type du nuage. On utilise ici 3 nuages avec chaque nuage étant différent au démarrage du jeu.
        self.tab_pos_sol = [[0,203], [33,203], [66,203], [99,203], [132,203], [165,203], [198,203], [231,203], [264,203], [297,203], [330,203]] # De la même façon que pour les nuages, on a un tableau de 11 sols, (pour recouvrir toute la longueur de l'écran) avec les coordonnées x et y
        self.tab_type_sol = [1, 2, 3,4,4, 3, 2, 1, 2, 2, 3,4,4, 3, 1] # Tableau qui contient les types de sols.
        f_high_score = open(r"./Resources/high_score.txt", "r") # Ouverture en lecture.
        self.high_score = f_high_score.readline()
        f_high_score.close()

    def reset(self):
        self.state = 'menu' # état par défaut : menu
        self.displayvolume = 0 # Variable qui dit si il faut afficher le rectangle du volume ou pas
        self.choix_menu = 0 # Choix du menu (0 pour jouer et 1 pour quitter). Permet de savoir sur quel choix est l'utilisateur pour afficher le curseur au bon endroit et savoir ce qu'il souhaite faire quand il appuye sur entrée
        self.clean = 0 # Permet de savoir si on passe de l'état menu -> jeu  et jeu -> menu pour faire des modifications UNIQUEMENT lors de la première itération
        self.speed = start_speed # fixe le speed du jeu
        self.score=0 # Initialisation du score à 0 (ne trichez pas svp)
        self.alive = True # Etat du blob (vivant ou mort)
        self.stopjump = False # permet de savoir si l'utilisateur veut arrêter de sauter (il appuye sur saut et relâche avant d'avoir atteint la hateur max du saut)
        self.jump = False # Permet de savoir si on est en train de sauter (pour éviter de spam le saut)
        self.fall = False # Permet de savoir si on est en chute libre (après avoir atteint le saut max, ou si l'utilisateur arrête de saut, on passe en chut libre)
        self.crouch = False # False : le blob n'est pas accroupi // True : le blob est accroupi
        self.jspeed= jspeed #Prends la valeur + ou - jspeed. Utiliser lors du saut, elle permet d'avoir un saut avec une vitesse non linéaire
        self.gravity = gravity # Gravité, aussi utilisé pour avoir un saut avec une vitesse non linéaire (surtout pour la chute)
        self.tab_pos_nuage = [[400,random.randrange(24, 178, 11)], [700,random.randrange(24, 178, 11)],[1000,random.randrange(24, 178, 11)]] # Tableau qui contient la position de chaque nuage. On utilise 3 nuages au maximum.Leur coordonnée y est prise aléatoirement.
        self.tab_type_nuage = [1, 2, 3] # Autre tableau qui définit le type du nuage. On utilise ici 3 nuages avec chaque nuage étant différent au démarrage du jeu.
        self.tab_pos_sol = [[0,203], [33,203], [66,203], [99,203], [132,203], [165,203], [198,203], [231,203], [264,203], [297,203], [330,203]] # De la même façon que pour les nuages, on a un tableau de 11 sols, (pour recouvrir toute la longueur de l'écran) avec les coordonnées x et y
        self.tab_type_sol = [1, 2, 3,4,4, 3, 2, 1, 2, 2, 3,4,4, 3, 1] # Tableau qui contient les types de sols.
        f_high_score = open(r"./Resources/high_score.txt", "r") # Ouverture en lecture.
        self.high_score = f_high_score.readline()
        f_high_score.close()

    def menu(self):
        """ Gesion du menu (affichage et evènements) """
        if (self.clean == 1):
            # A chaque fois qu'on meurt / qu'on revient dans le menu, on :
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP]) # Réactive les touches. (On les désactive pour éviter que le joueur spam un bouton entre ou le moment ou il meurt et le jeu retourne au menu)
            self.clean = 0 # On repasse la variable à 0
            pygame.event.clear() # On clear l'affichage en affichant le fond vert
        affiche_menu(self.choix_menu,self) # On appelle la fonction qui affiche le menu en fonction du choix du joueur
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Si le joueur appuie sur le bouton qui correspond à échap : 
                pygame.quit() # On quitte pygame
                sys.exit() # On ferme la fenêtre

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN: # Si le joueur appuie sur le bouton qui correspond à "bas" 
                self.choix_menu = (self.choix_menu+1)%nbr_choix_menu # on change la variable qui contient le choix du menu (pour rafficher le bon menu)
                self.canal_sound.play(self.sound_select)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP: # Si le joueur appuie sur le bouton qui correspond à "haut" 
                self.choix_menu = (self.choix_menu-1)%nbr_choix_menu # Mis à jour de la variable qui stocke le choix du joueur
                self.canal_sound.play(self.sound_select) 

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.state != 'game': # Si le joueur valide son choix via le bouton qui correspond à espace
                self.canal_sound.play(self.sound_validate)
                pygame.event.set_blocked(None) # On bloque les entrées d'events
                time.sleep(0.5) # Petite pause pour laisser le son de se jouer
                if (self.choix_menu == 0):
                    clean_affichage(fenetre) # On affiche le fond vert pour clean l'affichage
                    # pygame.display.set_caption("Blob Runner") # Nom de la fenêtre
                    self.state = 'game'
                    self.alive = True #Si jamais on retourne au menu, il faut remettre vivant à true
                elif (self.choix_menu == 1):
                    pygame.quit()
                    pygame.mixer.quit()
                    sys.exit()

            # Pour le réglage du volume, on utilise les flêches droites et gauches.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if self.vollvl <100 : # La variable vollvl permet d'autoriser 10 niveaux de volumes. De base il est a 0.5, et il peut monter jusqu'a 1 max
                    self.vollvl = self.vollvl + 10 # Monte d'1 niveau sonore
                    vol = float(log10(self.vollvl+1)/log10(101)) # Mis à jour du volume via une fontion log car le volume a une courbe exponentielle
                    theme_canal.set_volume(vol) 
                    self.canal_sound.set_volume(vol)
                self.displayvolume = 30 # Indique au programme qu'il faut afficher la barre du son

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if self.vollvl >0:  # La variable vollvl permet d'autoriser 10 niveaux de volumes. De base il est a 50, et il peut baisser jusqu'a 0
                    self.vollvl = self.vollvl - 10 # Baisse d'1 niveau sonore
                    vol = float(log10(self.vollvl+1)/log10(101)) # Mis à jour du volume via une fontion log car le volume a une courbe exponentielle
                    theme_canal.set_volume(vol)
                    self.canal_sound.set_volume(vol)
                self.displayvolume = 30 # Indique au programme qu'il faut afficher la barre du son



    def game(self):
        # change titre fenêtre
        if (self.clean == 0):
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP]) # On autorise uniquement les entrées d'event de type pressage / relachage de boutons
            #pygame.display.set_caption("Blob Runner")
            pygame.event.clear() # On clear les event qui étaient présents
            self.clean = 1 # On passe cette variable à 1 car on veut faire les commandes ci-dessus uniquement à la première itération
        self.Affiche_scene_jeu() # On lance l'affichage de la scène du jeu
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Echap = retour menu
                # blob mort
                self.alive = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.jump == False and self.crouch == False:
                # Pour sauter, on vérifie que la touche espace a été pressé, qu'on n'est pas déjà en train de sauter, et qu'on est pas accroupi
                self.jump = True
                self.canal_sound.play(self.sound_jump)

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and self.jump == True and self.crouch == False:
                # Si la touche espace est relâchée PENDANT un saut, et sans être accroupi, alors on va arrêter de monter et entamer la chute prématurement
                self.stopjump = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and self.jump == False and self.crouch == False:
                # Pour s'accroupir il faut presser la toucher (et maintenir) la touche bas, on vérifie qu'on est pas déjà accroupi et qu'on ne saute pas.
                self.crouch = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and self.jump == True :
                # Si maintenant on s'accroupi PENDANT un saut, alors on entame une chute encore plus rapide
                self.fall = True
                self.crouch= True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                # Si on relache le bouton s'accroupir, on repasse le blob debout
                self.crouch = False

            # Même gestion de volume que pour le menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if self.vollvl <100 :
                    self.vollvl = self.vollvl + 10
                    vol = float(log10(self.vollvl+1)/log10(101))
                    theme_canal.set_volume(vol)
                    self.canal_sound.set_volume(vol)
                self.displayvolume = 30

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if self.vollvl >0:
                    self.vollvl = self.vollvl - 10
                    vol = float(100*log10(self.vollvl+1)/log10(101))
                    theme_canal.set_volume(vol)
                    self.canal_sound.set_volume(vol)
                self.displayvolume = 30


    def state_manager(self):
        # Gère l'état (menu ou jeu)
        if self.state == 'menu':
            self.menu()
        elif self.state == 'game':
            # On augmente la speed du jeu ici
            self.speed = self.speed + acc_speed
            self.game()

    def ynuage(self, a): #Permet d'éviter de faire spawn un nuage aux même coordonnées y d'un autre nuage !
        # La variable a permet de savoir le numéro dans le tableau du nuage à placer.
        # En fonction de ce numéro, il faut vérifier que les nouvelles coordonnées y du nuage ne se superposent pas avec un autre nuage!
        if (a<=0): # Si c'est le nuage 0 :
            # On va le comparer avec le nuage 1 et 2
            Y1 = self.tab_pos_nuage[1][1]
            Y2 = self.tab_pos_nuage[2][1]
            while((self.tab_pos_nuage[a][1] <  Y1+24 and self.tab_pos_nuage[a][1] >  Y1-24) or (self.tab_pos_nuage[a][1] <  Y2+24 and self.tab_pos_nuage[a][1] >  Y2-24)):
                self.tab_pos_nuage[a][1] = random.randrange(24, 178, 11) # On prend un random entre 24 et 178 et on revérifie que ça match.

        elif(a==1):
            # Comparaison avec 0 et 2                                     
            Y0 = self.tab_pos_nuage[0][1]
            Y2 = self.tab_pos_nuage[2][1]
            while((self.tab_pos_nuage[a][1] <  Y0+24 and self.tab_pos_nuage[a][1] >  Y0-24) or (self.tab_pos_nuage[a][1] <  Y2+24 and self.tab_pos_nuage[a][1] >  Y2-24)):
                self.tab_pos_nuage[a][1] = random.randrange(24, 178, 11)


        elif(a>=2):
            # Comparaison avec 0 et 1
            Y0 = self.tab_pos_nuage[0][1]
            Y1 = self.tab_pos_nuage[1][1]
            while((self.tab_pos_nuage[a][1] <  Y0+24 and self.tab_pos_nuage[a][1] >  Y0-24) or (self.tab_pos_nuage[a][1] <  Y1+24 and self.tab_pos_nuage[a][1] >  Y1-24)):
                self.tab_pos_nuage[a][1] = random.randrange(24, 178, 11)




    def Affiche_scene_jeu(self):
        # On reset l'affichage avec l'affichage du fond vert
        fenetre.blit(fond_vert, (0,0))

        # Affiche du score :
        self.score= self.score + ceil(self.speed/15) #partie entière de la vitesse/15 arrondi au supérieur
        texte = font.render('Score: {0}'.format(int(self.score)), False, (48,98,48))  # "text", antialias, color
        fenetre.blit(texte, (200, 10))

        ## Affichage nuages
        # On affichage les nuages en fonction de leur type (cloud1 2 ou 3)
        for i in range (len(self.tab_pos_nuage)) :
            if(self.tab_type_nuage[i] == 1):
                fenetre.blit(cloud1, self.tab_pos_nuage[i])
            elif(self.tab_type_nuage[i]==2):
                fenetre.blit(cloud2, self.tab_pos_nuage[i])
            elif(self.tab_type_nuage[i] == 3):
                fenetre.blit(cloud3, self.tab_pos_nuage[i])

            if(self.tab_pos_nuage[i][0]<=-141):  #Si un nuage est en dehors de la zone de l'écran, on le réaffiche tout à droite
                # Coordonné X : On doit les faire spawn en dehors de l'écran.
                self.tab_pos_nuage[i][0] = random.randrange(x_fen, 2*x_fen, 20)
                # Coordonnée Y :
                self.tab_pos_nuage[i][1] = random.randrange(24, 178, 11)
                # On doit checker qu'il ne spawn pas sur un autre nuage :
                self.ynuage(i)  #Vérifie la coordonnée Y pour ne pas faire spawn le nuage aux même coordonnées y d'un autre nuage et risquer une superposition
                self.tab_type_nuage[i] = random.randrange(1, 4, 1)  #Nuage aléatoire (cloud1 2 ou 3)

            # Vitesse en fonction de sa coordonnée y :
            # Permet d'avoir un effet de profondeur
            if(self.tab_pos_nuage[i][1] < 76):
                self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0] - int(0.2*self.speed)

            elif(self.tab_pos_nuage[i][1] >= 76 and self.tab_pos_nuage[i][1] < 127):
                self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0] - int(0.3*self.speed)

            elif(self.tab_pos_nuage[i][1] >= 127):
                self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0]-int(0.4*self.speed)

        # Affichage du rectangle pour le volume si l'utilisateur l'a changé :
        if self.displayvolume>0 :
            fenetre.blit (img_volume, (49,50))
            pygame.draw.rect(fenetre, [15, 56, 15], [63, 52, 1.92*self.vollvl, 10], 0)
            self.displayvolume -=1


        ## affichage obstacles et fantome

#En fonction du numéro stocké dans le taleau type obstacle on sait lequel afficher

        obstacle.update()
        obstacle.x = obstacle.x- self.speed #Fais bouger l'élément vers la gauche
        if(obstacle.x<-50):  #Si l'obstacle est en dehors de la zone de l'écran, on en raffiche un à droite
            #Permet de rafficher l'obstacle à une distance parfaite pour avoir des obstacles espacés d'une distance minimale de la taille X de le fenêtre
            obstacle.x = random.randrange(x_fen+50, 3*x_fen, 5)
            # On choisit un type d'obstacle aléatoire. Comme l'obstacle fantome n'a pas la même hauteur que les murs, on adapate les coordonnées.
            obstacle.type = random.randrange(0, 3, 1)  #obstacle aléatoire
            if(obstacle.type == 2): # Fantome = modificiation coordonnée y
                obstacle.y = random.randrange(130, 136, 2)
                #self.obstacle = Fantome()
            elif(obstacle.type == 1 or obstacle.type == 0):
                obstacle.y  = 197
                #self.obstacle = Large_object()
            obstacle.change_mask(); #Update du mask car on a changé d'obstacle


        ## affichage du sol

        #boucle affichage du sol
        for i in range (len(self.tab_pos_sol)):
            #En fonction du numéro stocké dans le tableau type sol on sait quel sol affiché.
            if(self.tab_type_sol[i] == 1):
                fenetre.blit(sol1, self.tab_pos_sol[i])
            elif(self.tab_type_sol[i]==2):
                fenetre.blit(sol2, self.tab_pos_sol[i])
            elif(self.tab_type_sol[i] == 3):
                fenetre.blit(sol3, self.tab_pos_sol[i])
            elif(self.tab_type_sol[i] == 4):
                fenetre.blit(sol4, self.tab_pos_sol[i])
            self.tab_pos_sol[i][0] = self.tab_pos_sol[i][0]-self.speed #Fais bouger le sol vers la gauche
            if(self.tab_pos_sol[i][0]<=-33):  #Si un sol est en dehors de la zone de l'écran, on le réaffiche tout à droite
                self.tab_pos_sol[i][0] = 330 + (self.tab_pos_sol[i][0]+33)
                self.tab_type_sol[i] = random.randrange(1, 5, 1)  #Sol aléatoire

        ## Affichage du blob (jump)

        if (self.alive): # Si on est en vie

            if(self.jump): # On vérifie si on saute :
                blob.blob_y= blob.blob_y + self.jspeed
                #print(blob.blob_y)

                if(blob.blob_y>180):
                    blob.blob_y=180
                    self.jspeed= jspeed
                    self.jump = False
                    self.stopjump = False
                    self.fall = False

                else :

                    if(self.stopjump and self.jspeed < 0):
                        self.jspeed= int(jspeed/4)
                        self.stopjump = False
                    
                    if self.fall:
                        self.jspeed=self.jspeed + 3*self.gravity
                        blob_crouch.x = blob.blob_x
                        blob_crouch.y = blob.blob_y+9
                        blob_crouch.update()
                    else:
                        self.jspeed=self.jspeed + self.gravity
                        blob.update()

                if self.fall :
                    fenetre.blit(blob_crouch.image, (blob_crouch.x, blob_crouch.y))
                else :
                    fenetre.blit(blob.image, (blob.blob_x, blob.blob_y))

            else: # Si on saute pas
                if(self.crouch): # On vérifie si on veut s'accroupir
                    blob_crouch.x = blob.blob_x
                    blob_crouch.y = blob.blob_y+9 #Il faut décaler de 9x la coordonnée y du blob crouch par rapport au blob, car l'affichage se fait par le haut gauche. Comme le blob crouch est plus petit, il faut donc augmenter de 9px y.
                    blob_crouch.update()
                    fenetre.blit(blob_crouch.image, (blob_crouch.x, blob_crouch.y))
                else: # Sinon on reset les coordonnées du blob à ses coordonnées de base (180 et 10)
                    blob.blob_x = 10
                    blob.blob_y = 180
                    blob.update()
                    fenetre.blit(blob.image, (blob.blob_x, blob.blob_y))


        else: #si le blob est mort
            pygame.event.set_blocked(None) # Si on est mort, on bloque toutes les entrées d'event
            if(self.score > int(self.high_score)):
                f_high_score = open(r"./Resources/high_score.txt", "w") # Ouverture en écriture.
                f_high_score.write(str(self.score))
                f_high_score.close()
            obstacle.__init__() # Reset obstacle
            fenetre.blit(blob_dead, (blob.blob_x, blob.blob_y)) # affichage blob mort
            fenetre.blit(game_over_texte, (50,90)) # affichage text game over
            pygame.display.flip() # Pour afficher le text du game over
            self.canal_sound.play(self.sound_game_over)
            time.sleep(2) # sleep de 2 secondes pour laisser le temps à la musique de se jouer
            clean_affichage(fenetre) # Affichage fond vert pour reset affichage
            pygame.display.set_caption("Menu de la ScareBot")
            self.reset() # Reset de toutes les variables
            self.clean = 1 # On passe la variable à 1, qui permet d'effectuer des commandes uniquement lors de la première itération
        pygame.display.flip() # Enfin, on affiche à l'écran.


        all_sprite.update() # On update tout les sprite
        # Gestion collision :
        # Si accroupi on regarde la collision entre blob crouch et obstacle                             
        if(self.crouch):
            if(pygame.sprite.collide_mask(blob_crouch, obstacle)):
                self.alive = False
        # Sinon entre blob et obstacle
        else:
            if(pygame.sprite.collide_mask(blob, obstacle)):
                self.alive = False
## Fin de la classe GameState



game_state = GameState() #on définit un objet de la classe gamestate

# Création d'un groupe de sprite. Permet de lancer la méthode update() de chaque sprite en une seule commande.
all_sprite = pygame.sprite.Group()
obstacle = Obstacle() # Création d'un objet de type obstacle.
blob_crouch = Blob_crouch() # Création d'un objet de type blob_crouch
blob = Blob() # Création d'un objet blob
## Boucle infinie pour faire tourner le jeu
while continuer:
    game_state.state_manager()
    nb_fps = font.render('FPS: {0}'.format(int(clock.get_fps())), False, (48,98,48))  # "text", antialias, color
    fenetre.blit(nb_fps, (200, 225))
    pygame.display.flip()
    clock.tick(fps) # Bloque le jeu à fps FPS
pygame.quit()
pygame.mixer.quit()
sys.exit()
