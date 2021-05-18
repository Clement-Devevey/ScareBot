## Importation des bibliothèques nécessaires
import pygame, sys, time, random
from pygame.locals import *
from math import ceil

## Initialisation de la bibliothèque Pygame + timer + constante
pygame.init()
clock = pygame.time.Clock()
NOMBRE_DE_CHOIX_MENU = 2 # les deux choix du menu sont Play ou Quit

## Création de la fenêtre (en pixels)
x_fen = 313
y_fen = 245
fenetre = pygame.display.set_mode((x_fen,y_fen))

chemin_images = "C:\\Users\\damde\\Desktop\\CLEMENT_PING\\gameboy\\images\\"
## Chargement des images
fond_vert = pygame.image.load("./Resources/images/fond_vert.png").convert()
menu_fond = pygame.image.load("./Resources/images/menu.png").convert_alpha()
blob = pygame.image.load("./Resources/images/blob_base.png").convert_alpha()
blob_crouch = pygame.image.load("./Resources/images/blob crouch.png").convert_alpha()
curseur_selection = pygame.image.load("./Resources/images/curseur_selection_menu_gameboy.png").convert_alpha()
sol1 = pygame.image.load("./Resources/images/sol 1.png").convert_alpha()
sol2 = pygame.image.load("./Resources/images/sol 2.png").convert_alpha()
sol3 = pygame.image.load("./Resources/images/sol 3.png").convert_alpha()
blob_dead = pygame.image.load("./Resources/images/blob dead.png").convert_alpha()
game_over_texte = pygame.image.load("./Resources/images/game over gameboy.png").convert_alpha()
cloud1 = pygame.image.load("./Resources/images/cloud 1.png").convert_alpha()
cloud2 = pygame.image.load("./Resources/images/cloud 2.png").convert_alpha()
cloud3 = pygame.image.load("./Resources/images/cloud 3.png").convert_alpha()
large_object= pygame.image.load("./Resources/images/large object.png").convert_alpha()
small_object= pygame.image.load("./Resources/images/small object.png").convert_alpha()
fantome= pygame.image.load("./Resources/images/fantome gameboy.png").convert_alpha()


## Icon de la fenêtre et nom de la fenêtre
pygame.display.set_icon(blob)
pygame.display.set_caption("Menu de la ScareBot")

## Chargement des musiques
#theme = pygame.mixer.music.load(r"H:\gameboy\Musiques\8bit.wav")

select = pygame.mixer.Sound("./Resources/musiques/sfxMenuScarebotSelect.wav")
jump = pygame.mixer.Sound("./Resources/musiques/sfxBlobRunn3rJump.wav")
valide = pygame.mixer.Sound("./Resources/musiques/sfxMenuScarebotValidate.wav")
game_over = pygame.mixer.Sound("./Resources/musiques/sfxScarebotGameOver.wav")
theme = pygame.mixer.Sound("./Resources/musiques/8bit.wav")

## Chargement de la police

font = pygame.font.Font(r"./Resources/images/pixelmix_bold.ttf", 12)
# S'utilise avec texte = font.render("text", False, color)  # "text", antialias, color.
#                fenetre.blit(texte, (x, y))

## fonction qui affiche le menu avec l'option en cours de sélection surligné en jaune
def affiche_menu(choix):
    if(choix == 0):
        fenetre.blit(fond_vert, (0,0))
        fenetre.blit(menu_fond, (0,0))
        fenetre.blit(curseur_selection, (65,102))
        pygame.display.flip()

    elif(choix == 1):
        fenetre.blit(fond_vert, (0,0))
        fenetre.blit(menu_fond, (0,0))
        fenetre.blit(curseur_selection, (65,163))
        pygame.display.flip()

## Fonction qui clean l'ancien affichage :
def clean_affichage(screen):
    fenetre.blit(fond_vert, (0,0))
    pygame.display.flip()


## Classe pour gérer les scènes : ici, on a la scènes du menu et celle du jeu

class GameState():
    def __init__(self):
        self.state = 'menu'
        self.choix_menu = 0
        self.clean = 0
        self.x_fen = 313
        self.speed = 8
        self.y_fen = 245
        self.score=0
        self.i=0 #Boucle affichage blob
        self.blob_x = 10
        self.blob_y = 180
        self.vivant = True
        self.stopjump = False
        self.jump = False
        self.bas = False
        self.additionneur=-8 #Prends la valeur 5 ou -5 pour le saut : la coordonnée y du blob va prendre descendre de (0->-50->0)
        self.tab_pos_nuage = [[400,random.randrange(24, 178, 11)], [700,random.randrange(24, 178, 11)],[1000,random.randrange(24, 178, 11)]]
        self.tab_type_nuage = [1, 2, 3]
        self.tab_pos_obstacle = [[400,197], [700,197],[1000,random.randrange(130, 136, 1)]]
        self.tab_type_obstacle = [1, 2, 3]
        self.tab_pos_sol = [[0,203], [33,203], [66,203], [99,203], [132,203], [165,203], [198,203], [231,203], [264,203], [297,203], [330,203]]
        self.tab_type_sol = [1, 2, 3, 3, 2, 1, 2, 2, 3, 3, 1]

    def menu(self):
        self.clean = 0
        affiche_menu(self.choix_menu)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_DOWN:
                self.choix_menu = (self.choix_menu+1)%NOMBRE_DE_CHOIX_MENU
                canal = select.play()


            if event.type == KEYDOWN and event.key == K_UP:
                self.choix_menu = (self.choix_menu-1)%NOMBRE_DE_CHOIX_MENU
                canal = select.play()

            if event.type == KEYDOWN and event.key == K_RETURN: #K RETURN = entrée
                canal = valide.play()
                time.sleep(0.5)

                if (self.choix_menu == 0):
                    #print("jouer")
                    clean_affichage(fenetre)
                    pygame.display.set_caption("Blob Runner") # Nom de la fenêtre
                    self.state = 'game'
                    self.vivant = True #Si jamais on retourne au menu, il faut remettre vivant à true

                elif (self.choix_menu == 1):
                    pygame.quit()
                    sys.exit()



    def game(self):
        # change titre fenêtre
        if (self.clean == 0):
            pygame.display.set_caption("Blob Runner")
            self.clean = 1
        #pos_blob = blob.get_rect();
        #print(pos_blob.x)
        #print(pos_blob.y)
        self.Affiche_scene_jeu()

        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # blob mort
                self.vivant = False
                self.Affiche_scene_jeu()
                canal = game_over.play()
                time.sleep(3)
                self.state = 'menu'
                self.score = 0
                clean_affichage(fenetre)
                affiche_menu(0)
                pygame.display.set_caption("Menu de la ScareBot")

            if event.type == KEYDOWN and event.key == K_SPACE and self.jump == False and self.bas == False:
                self.jump = True
                canal = jump.play()

            if event.type == KEYUP and event.key == K_SPACE and self.jump == True and self.bas == False:
                self.stopjump = True

            if event.type == KEYDOWN and event.key == K_DOWN and self.jump == False and self.bas == False:
                self.bas = True

            if event.type == KEYUP and event.key == K_DOWN and self.jump == False:
                self.bas = False


    def state_manager(self):
        if self.state == 'menu':
            self.menu()
        elif self.state == 'game':
            self.speed = self.speed + 0.001
            self.game()


    def Affiche_scene_jeu(self):
        fenetre.blit(fond_vert, (0,0))

        ##Affiche du score :
        self.score=self.score+ceil(self.speed/2) #partie entière de la vitesse/2 arrondi au supérieur
        texte = font.render('Score: {0}'.format(int(self.score)), False, (48,98,48))  # "text", antialias, color
        fenetre.blit(texte, (200, 10))

        ## Affichage nuages
        for i in range (len(self.tab_pos_nuage)) :
            if(self.tab_type_nuage[i] == 1):
                fenetre.blit(cloud1, self.tab_pos_nuage[i])
            elif(self.tab_type_nuage[i]==2):
                fenetre.blit(cloud2, self.tab_pos_nuage[i])
            elif(self.tab_type_nuage[i] == 3):
                fenetre.blit(cloud3, self.tab_pos_nuage[i])

            self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0]-int(0.004*(random.randrange(75, 100, 1))*self.speed) #Fais bouger le nuage vers la gauche

            if(self.tab_pos_nuage[i][0]<=-141):  #Si un nuage est en dehors de la zone de l'écran, on le réaffiche tout à droite
                if(i==0):
                    self.tab_pos_nuage[i][0] = self.tab_pos_nuage[2][0] + x_fen
                elif(i==1):
                    self.tab_pos_nuage[i][0] = self.tab_pos_nuage[0][0] + x_fen
                elif(i==2):
                    self.tab_pos_nuage[i][0] = self.tab_pos_nuage[1][0] + x_fen

                self.tab_pos_nuage[i][1] = random.randrange(24, 178, 11)
                self.tab_type_nuage[i] = random.randrange(1, 4, 1)  #Nuage aléatoire


        ## affichage obstacles et fantome

        for i in range (len(self.tab_pos_obstacle)):
            #En fonction du numéro stocké dans le taleau type obstacle on sait lequel afficher
            if(self.tab_type_obstacle[i] == 1):
                fenetre.blit(small_object, self.tab_pos_obstacle[i])
            elif(self.tab_type_obstacle[i]==2):
                fenetre.blit(large_object, self.tab_pos_obstacle[i])
            elif(self.tab_type_obstacle[i] == 3):
                fenetre.blit(fantome, self.tab_pos_obstacle[i])

            self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[i][0]-self.speed #Fais bouger l'élément vers la gauche

            if(self.tab_pos_obstacle[i][0]<-47):  #Si un obstacle est en dehors de la zone de l'écran, on en raffiche un à droite
                #Permet de rafficher l'obstacle à une distance parfaite pour avoir des obstacles espacés d'une distance minimale de la taille X de le fenêtre
                if(i==0):
                    self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[2][0]+random.randrange(x_fen, x_fen+100, 5)
                elif(i==1):
                    self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[0][0]+random.randrange(x_fen, x_fen+100, 5)
                elif(i==2):
                    self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[1][0]+random.randrange(x_fen, x_fen+100, 5)

                # On choisit un type d'obstacle aléatoire. Comme l'obstacle fantome n'a pas la même hauteur que les murs, on adapate les coordonnées.
                self.tab_type_obstacle[i] = random.randrange(1, 4, 1)  #obstacle aléatoire
                if(self.tab_type_obstacle[i] == 3):
                    self.tab_pos_obstacle[i][1] = random.randrange(130, 136, 2)
                else:
                    self.tab_pos_obstacle[i][1] = 197

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

            self.tab_pos_sol[i][0] = self.tab_pos_sol[i][0]-self.speed #Fais bouger le sol vers la gauche

            if(self.tab_pos_sol[i][0]<=-33):  #Si un sol est en dehors de la zone de l'écran, on le réaffiche tout à droite
                self.tab_pos_sol[i][0] = 330 + (self.tab_pos_sol[i][0]+33)
                self.tab_type_sol[i] = random.randrange(1, 4, 1)  #Sol aléatoire

        # Affichage du blob :
        if (self.vivant):
            if(self.jump):
                self.i=self.i+self.additionneur

                if(self.i<-72 or self.stopjump):
                    self.additionneur=8
                    self.stopjump = False

                if(self.i > 0):
                    self.jump = False
                    self.additionneur=-8

                self.blob_y=180+self.i
                if(self.blob_y>180):
                    self.blob_y=180
                fenetre.blit(blob, (self.blob_x, self.blob_y))

            else:

                if(self.bas):
                    fenetre.blit(blob_crouch, (self.blob_x, self.blob_y+9))

                else:
                    self.blob_x = 10
                    self.blob_y = 180
                    fenetre.blit(blob, (self.blob_x, self.blob_y))

        else: #si le blob est mort
            fenetre.blit(blob_dead, (self.blob_x, self.blob_y))
            fenetre.blit(game_over_texte, (50,90))
            #Reset obstacle :
            self.tab_pos_obstacle = [[400,197], [600,197],[800,random.randrange(120, 136, 2)]]
            self.tab_type_obstacle = [1, 2, 3]
            #Remise à 0 des éléments si on mort pendant le saut
            self.jump = False
            self.speed = 8
            self.additionneur = -8
            #Remise à des éléments si on meurt accroupi :
            self.bas=False
            #Remise à l'état initial de la position du blob
            self.blob_x = 10
            self.blob_y = 180

        pygame.display.flip()


## Fin de la classe GameState





## Variables
continuer = 1
game_state = GameState() #on définit un objet de la classe gamestate
fps = 60

##Lancement du son du jeu
theme_canal = theme.play(-1) #-1 = musique en boucle :)

## Boucle infinie pour faire tourner le jeu

while continuer:
    game_state.state_manager()
    clock.tick(fps) # Bloque le jeu à fps FPS
pygame.quit()
sys.exit()





























