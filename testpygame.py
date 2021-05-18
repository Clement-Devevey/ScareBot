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

## Chargement du high_score

# Pour lire le high score :
f_high_score = open(r"./Resources/high_score.txt", "r") # Ouverture en lecture.
high_score = f_high_score.readline()
f_high_score.close()


## fonction qui affiche le menu avec l'option en cours de sélection surligné en jaune
def affiche_menu(choix):
    if(choix == 0):
        fenetre.blit(fond_vert, (0,0))
        fenetre.blit(menu_fond, (0,0))
        fenetre.blit(curseur_selection, (65,102))
        texte = font.render('High score: {0}'.format(high_score), False, (48,98,48))  # "text", antialias, color
        fenetre.blit(texte, (75, 225))
        pygame.display.flip()

    elif(choix == 1):
        fenetre.blit(fond_vert, (0,0))
        fenetre.blit(menu_fond, (0,0))
        fenetre.blit(curseur_selection, (65,163))
        texte = font.render('High score: {0}'.format(high_score), False, (48,98,48))  # "text", antialias, color
        fenetre.blit(texte, (75, 225))
        pygame.display.flip()

## Fonction qui clean l'ancien affichage :
def clean_affichage(screen):
    fenetre.blit(fond_vert, (0,0))
    pygame.display.flip()

## Variables globales pour la vitesse
jspeed = -16
speed = 4.5

## Classe pour gérer les scènes : ici, on a la scènes du menu et celle du jeu

class GameState():
    def __init__(self):
        self.state = 'menu'
        self.choix_menu = 0
        self.clean = 0
        self.x_fen = 313
        self.speed = speed
        self.y_fen = 245
        self.score=0
        self.i=0 #Boucle affichage blob
        self.blob_x = 10
        self.blob_y = 180
        self.alive = True
        self.stopjump = False
        self.jump = False
        self.fall = False
        self.crouch = False
        self.jspeed= jspeed #Prends la valeur 5 ou -5 pour le saut : la coordonnée y du blob va prendre descendre de (0->-50->0)
        self.gravity = 1
        self.tab_pos_nuage = [[400,random.randrange(24, 178, 11)], [700,random.randrange(24, 178, 11)],[1000,random.randrange(24, 178, 11)]]
        self.tab_type_nuage = [1, 2, 3]
        self.tab_pos_obstacle = [[700,197], [1000,197],[1300,random.randrange(130, 136, 1)]]
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
                    self.alive = True #Si jamais on retourne au menu, il faut remettre vivant à true

                elif (self.choix_menu == 1):
                    pygame.quit()
                    sys.exit()



    def game(self):
        # change titre fenêtre
        if (self.clean == 0):
            pygame.display.set_caption("Blob Runner")
            self.clean = 1
        self.Affiche_scene_jeu()

        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                # blob mort
                self.alive = False


            if event.type == KEYDOWN and event.key == K_SPACE and self.jump == False and self.crouch == False:
                self.jump = True
                canal = jump.play()

            if event.type == KEYUP and event.key == K_SPACE and self.jump == True and self.crouch == False:
                self.stopjump = True

            if event.type == KEYDOWN and event.key == K_DOWN and self.jump == False and self.crouch == False:
                self.crouch = True

            if event.type == KEYDOWN and event.key == K_DOWN and self.jump == True :
                self.fall = True
                self.crouch= True

            if event.type == KEYUP and event.key == K_DOWN:
                self.crouch = False


    def state_manager(self):
        if self.state == 'menu':
            self.menu()
        elif self.state == 'game':
            self.speed = self.speed + 0.0025
            self.game()

    def ynuage(self, a): #Permet d'éviter de faire spawn un nuage aux même coordonnées d'un autre nuage !
        #Y_a_placer = self.tab_pos_nuage[a][1]
        if (a<=0):
            Y1 = self.tab_pos_nuage[1][1]
            Y2 = self.tab_pos_nuage[2][1]
            while((self.tab_pos_nuage[a][1] <  Y1+24 and self.tab_pos_nuage[a][1] >  Y1-24) or (self.tab_pos_nuage[a][1] <  Y2+24 and self.tab_pos_nuage[a][1] >  Y2-24)):
                self.tab_pos_nuage[a][1] = random.randrange(24, 178, 11)
                #Y_a_placer = self.tab_pos_nuage[a][1]
        elif(a==1):
            Y0 = self.tab_pos_nuage[0][1]
            Y2 = self.tab_pos_nuage[2][1]
            while((self.tab_pos_nuage[a][1] <  Y0+24 and self.tab_pos_nuage[a][1] >  Y0-24) or (self.tab_pos_nuage[a][1] <  Y2+24 and self.tab_pos_nuage[a][1] >  Y2-24)):
                self.tab_pos_nuage[a][1] = random.randrange(24, 178, 11)
                #Y_a_placer = self.tab_pos_nuage[a][1]

        elif(a>=2):
            Y0 = self.tab_pos_nuage[0][1]
            Y1 = self.tab_pos_nuage[1][1]
            while((self.tab_pos_nuage[a][1] <  Y0+24 and self.tab_pos_nuage[a][1] >  Y0-24) or (self.tab_pos_nuage[a][1] <  Y1+24 and self.tab_pos_nuage[a][1] >  Y1-24)):
                self.tab_pos_nuage[a][1] = random.randrange(24, 178, 11)
                #Y_a_placer = self.tab_pos_nuage[a][1]

    def Affiche_scene_jeu(self):
        fenetre.blit(fond_vert, (0,0))

        ##Affiche du score :
        self.score= self.score + ceil(self.speed/15) #partie entière de la vitesse/2 arrondi au supérieur
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

            if(self.tab_pos_nuage[i][0]<=-141):  #Si un nuage est en dehors de la zone de l'écran, on le réaffiche tout à droite
                # Coordonné X : On doit les faire spawn en dehors de l'écran.
                self.tab_pos_nuage[i][0] = random.randrange(x_fen, 2*x_fen, 20)
                # Coordonnée Y :
                self.tab_pos_nuage[i][1] = random.randrange(24, 178, 11)
                # On doit checker qu'il ne spawn pas sur un autre nuage >_<
                self.ynuage(i)  #Vérifie la coordonnée Y pour ne pas avoir 2 nuages l'un sur l'autre !
                self.tab_type_nuage[i] = random.randrange(1, 4, 1)  #Nuage aléatoire

            # Vitesse en fonction de sa coordonnée y :
            if(self.tab_pos_nuage[i][1] < 76):
                self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0] - int(0.2*self.speed) #int(0.004*(50->100)*self.speed)

            elif(self.tab_pos_nuage[i][1] >= 76 and self.tab_pos_nuage[i][1] < 127):
                self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0] - int(0.3*self.speed)

            elif(self.tab_pos_nuage[i][1] >= 127):
                self.tab_pos_nuage[i][0] = self.tab_pos_nuage[i][0]-int(0.4*self.speed)




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
                    self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[2][0]+random.randrange(x_fen, 2*x_fen, 5)
                elif(i==1):
                    self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[0][0]+random.randrange(x_fen, 2*x_fen+100, 5)
                elif(i==2):
                    self.tab_pos_obstacle[i][0] = self.tab_pos_obstacle[1][0]+random.randrange(x_fen, 2*x_fen+100, 5)

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

        ## Affichage du blob : (saut)
        if (self.alive):
            if(self.jump):
                self.blob_y= self.blob_y + self.jspeed
                #print ("jump=",self.jump," speed=",self.jspeed," stopjump=",self.stopjump)
                if(self.stopjump and self.jspeed < 0):
                    self.jspeed= int(jspeed/4)
                    self.stopjump = False

                if self.fall:
                    self.jspeed=self.jspeed + 3*self.gravity
                else:
                    self.jspeed=self.jspeed + self.gravity

                if(self.blob_y>=180):
                    self.blob_y=180
                    self.jspeed= jspeed
                    self.jump = False
                    self.stopjump = False
                    self.fall = False


                if self.fall:
                    fenetre.blit(blob_crouch, (self.blob_x, self.blob_y+9))
                else:
                    fenetre.blit(blob, (self.blob_x, self.blob_y))


            else:

                if(self.crouch):
                    fenetre.blit(blob_crouch, (self.blob_x, self.blob_y+9))

                else:
                    self.blob_x = 10
                    self.blob_y = 180
                    fenetre.blit(blob, (self.blob_x, self.blob_y))

        else: #si le blob est mort
            if(self.score > int(high_score)):
                f_high_score = open(r"./Resources/high_score.txt", "w") # Ouverture en lecture.
                f_high_score.write(str(self.score))
                print(self.score)
                f_high_score.close()
            fenetre.blit(blob_dead, (self.blob_x, self.blob_y))
            fenetre.blit(game_over_texte, (50,90))
            pygame.display.flip() # Pour afficher le text du game over
            canal = game_over.play()
            time.sleep(3)
            clean_affichage(fenetre)
            pygame.display.set_caption("Menu de la ScareBot")
            self.__init__()

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





























