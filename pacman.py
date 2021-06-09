import pygame
import time
import math
import asyncio
import random
import json

async def gui():


    global x_fantome, y_fantome, position_x_pacman, position_y_pacman, derniere_actualisation_image, died, info_a_envoyer, donneesJoueurs, nomJoueur
    died = False
    derniere_actualisation_image = time.time()
    width,height = 1080,720
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Pacman')

    fps = 60


    position_x_pacman = 270
    position_y_pacman = 342
    x_pacman_grille = 0
    y_pacman_grille = 0
    x_fantome = 0
    y_fantome = 0
    x_grille_fantome = 0
    y_grille_fantome = 0
    x_bonus = 100
    y_bonus = 100
    pacman_power_up = False#Précise si pacman est en phase de bonus
    heure_consommation_bonus = 0
    temps_bonus = 3.5
    temps_avant_reapparition_bonus = 10#Temps avant que le bonus réapparaisse
    bonus_sur_le_jeu = True#Indique si le bonus est dans le jeu
    coordonnees_portail_1 = (0,0) #Coordonnées dans la grille de jeu du 1er portail
    coordonnees_portail_2 = (0,0)
    derniere_teleportation_portail = 0#Derniere fois qu'on s'est fait téléporter
    cooldown_portail = 0.3#Interval de temps en s pour prendre un portail
    rayon_pacman = 15
    vitesse = 3

    direction_pacman = 2#Direction dans laquelle va pacman : 0 immobile, 1 haut, 2 bas, 3 gauche, 4 droite
    memorisation_direction = 0#Future direction où va aller pacman, quand il le pourra

    def distance(x1,y1,x2,y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    def coordonnees_fantome():
        #x_fantome, y_fantome sont récupérés par communication()
        x_grille_fantome, y_grille_fantome = int(x_fantome/largeur_obstacle), int(y_fantome/hauteur_obstacle)
        return x_fantome, y_fantome, x_grille_fantome, y_grille_fantome

    '''def generer_bonus():#Fonction pour générer une position pour le bonus
        x_grille_bonus = 0
        y_grille_bonus = 0
        while grille_jeu[y_grille_bonus][x_grille_bonus] == 1:#On recalcule des coordonnees jusqu'à tomber dans une case vide
            x_grille_bonus = random.randint(0,largeur_grille-1)
            y_grille_bonus = random.randint(0,hauteur_grille-1)
        x_bonus = largeur_obstacle*x_grille_bonus+(largeur_obstacle/2)
        y_bonus = hauteur_obstacle*y_grille_bonus+(hauteur_obstacle/2)
        return x_bonus, y_bonus'''


    def update_screen():

        couleur_bordure = (abs((time.time()*500)%255-127)+127,abs((time.time()*180)%255-127)+127,abs((time.time()*310)%255-127)+127)#on se base sur l'heure pour faire une couleur pseudo-aléatoire des bordures
        #couleur_bordure = (0,255,0)
        #couleur_obstacle = (255,0,0)
        #couleur_background = (0,0,100)
        couleur_obstacle = (0,0,0)
        couleur_background = (0,0,0)
        screen.fill(couleur_background)





        #Dessin des obstacles
        for y in range(hauteur_grille):
            for x in range(largeur_grille):
                if grille_jeu[y][x] == 1:#Dessin des obstacles
                    #niveau_rouge = int(abs(x**3-y**3)/14)
                    #print(niveau_rouge)
                    pygame.draw.rect(screen, couleur_obstacle, (x*largeur_obstacle, y*hauteur_obstacle, largeur_obstacle, hauteur_obstacle))

                if grille_jeu[y][x] == 2:#Dessin des portails
                    pygame.draw.circle(screen, couleur_bordure, (int(x*largeur_obstacle+int(largeur_obstacle/2)), int(y*hauteur_obstacle+int(hauteur_obstacle/2))), int((time.time()%1.5)/1.5*rayon_pacman+1), True)
                    pygame.draw.circle(screen, couleur_bordure, (int(x*largeur_obstacle+int(largeur_obstacle/2)), int(y*hauteur_obstacle+int(hauteur_obstacle/2))), int(((time.time()+0.5)%1.5)/1.5*rayon_pacman+1), True)
                    pygame.draw.circle(screen, couleur_bordure, (int(x*largeur_obstacle+int(largeur_obstacle/2)), int(y*hauteur_obstacle+int(hauteur_obstacle/2))), int(((time.time()+1)%1.5)/1.5*rayon_pacman+1), True)

        #Dessin des contours des obstacles
        for y in range(hauteur_grille):
            for x in range(1,largeur_grille):
                if grille_jeu[y][x]==1 and grille_jeu[y][x-1]!=1:
                    pygame.draw.line(screen, couleur_bordure, (x*largeur_obstacle, y*hauteur_obstacle), (x*largeur_obstacle, (y+1)*hauteur_obstacle))


        for y in range(hauteur_grille):
            for x in range(largeur_grille-1):
                if grille_jeu[y][x]==1 and grille_jeu[y][x+1]!=1:
                    pygame.draw.line(screen, couleur_bordure, ((x+1)*largeur_obstacle, y*hauteur_obstacle), ((x+1)*largeur_obstacle, (y+1)*hauteur_obstacle))

        for y in range(1, hauteur_grille):
            for x in range(largeur_grille):
                if grille_jeu[y][x]==1 and grille_jeu[y-1][x]!=1:
                    pygame.draw.line(screen, couleur_bordure, (x*largeur_obstacle, y*hauteur_obstacle), ((x+1)*largeur_obstacle, y*hauteur_obstacle))

        for y in range(hauteur_grille-1):
            for x in range(largeur_grille):
                if grille_jeu[y][x]==1 and grille_jeu[y+1][x]!=1:
                    pygame.draw.line(screen, couleur_bordure, (x*largeur_obstacle, (y+1)*hauteur_obstacle), ((x+1)*largeur_obstacle, (y+1)*hauteur_obstacle))


        if len(donneesJoueurs)>0:
            dic = donneesJoueurs[0]
            for key in dic.keys():
                if dic[key]['pacman'] == True:#Le perso est un pacman
                    if bytes(str(key), 'utf-8') != nomJoueur:
                        try:
                            x, y = tuple(dic[key]['pos'].split(" "))
                            x , y= int(x), int(y)
                            if dic[key]['powerup_on'] == False:
                                pygame.draw.circle(screen, (255,255,0), (int(x), int(y)), rayon_pacman)
                            else:
                                pygame.draw.circle(screen, (255,0,200), (int(x), int(y)), rayon_pacman)
                            pygame.draw.circle(screen, (0,0,0), (int(x+int(rayon_pacman/2)), int(y-int(rayon_pacman/2))), int(rayon_pacman/5))
                            pygame.draw.line(screen, (0,0,0), (x+int(rayon_pacman/4), y),( x+rayon_pacman, y))
                            if int(time.time()*3)%2==0:
                                pygame.draw.polygon(screen, couleur_background, [(x, y), (x+rayon_pacman, y+int(rayon_pacman/2)), (x+rayon_pacman, y-int(rayon_pacman/2))], False)
                        except:
                            pass
                else:#le perso est un fantome
                    if bytes(str(key), 'utf-8') != nomJoueur:#On ne se dessine pas soi-meme
                        try:
                            x, y = tuple(dic[key]['pos'].split(" "))
                            x , y= int(x), int(y)
                            pygame.draw.circle(screen, (255,255,255), (int(x), int(y)), rayon_pacman)
                            pygame.draw.circle(screen, (0,0,0), (x+int(rayon_pacman/2), y-int(rayon_pacman/3)), int(rayon_pacman/5))
                            pygame.draw.circle(screen, (0,0,0), (x-int(rayon_pacman/2), y-int(rayon_pacman/3)), int(rayon_pacman/5))
                        except:
                            pass

            if donneesJoueurs[1] != None:#On vérifie que les coordonnées du bonus soit envoyées
                bonus_sur_le_jeu = True
                try:
                    x_bonus, y_bonus = tuple(donneesJoueurs[1])
                    pygame.draw.circle(screen, (255,0,255), (int(x_bonus), int(y_bonus)), int(rayon_pacman/4))
                except:
                    pass
            else:
                bonus_sur_le_jeu = False

        if pacman_power_up == False:#dessin pacman
            pygame.draw.circle(screen, (255,200,0), (int(position_x_pacman), int(position_y_pacman)), rayon_pacman)
            if int(time.time()*3)%2==0:
                pygame.draw.polygon(screen, couleur_background, [(position_x_pacman, position_y_pacman), (position_x_pacman+rayon_pacman, position_y_pacman+int(rayon_pacman/2)), (position_x_pacman+rayon_pacman, position_y_pacman-int(rayon_pacman/2))], False)
        else:#dessin pacman en bonus
            pygame.draw.circle(screen, (200,0,150), (int(position_x_pacman), int(position_y_pacman)), rayon_pacman)
            if int(time.time()*5)%2==0:
                pygame.draw.polygon(screen, couleur_background, [(position_x_pacman, position_y_pacman), (position_x_pacman+rayon_pacman, position_y_pacman+int(rayon_pacman/2)), (position_x_pacman+rayon_pacman, position_y_pacman-int(rayon_pacman/2))], False)
        pygame.draw.circle(screen, (0,0,0), (int(position_x_pacman+int(rayon_pacman/2)), int(position_y_pacman-int(rayon_pacman/2))), int(rayon_pacman/5))
        pygame.draw.line(screen, (0,0,0), (position_x_pacman+int(rayon_pacman/4), position_y_pacman),( position_x_pacman+rayon_pacman, position_y_pacman))

        pygame.display.flip()

    def update_position(position_x_pacman, position_y_pacman, direction_pacman):

        x_pacman_grille = int(position_x_pacman/largeur_obstacle)
        y_pacman_grille = int(position_y_pacman/hauteur_obstacle)

        if memorisation_direction == 1:
            if direction_pacman==2:
                direction_pacman=1
            else:
                if direction_pacman == 3 or direction_pacman == 4:
                    if grille_jeu[y_pacman_grille-1][x_pacman_grille] != 1:
                        if position_x_pacman%largeur_obstacle>=int(largeur_obstacle/2) and (position_x_pacman-vitesse)%largeur_obstacle<=int(largeur_obstacle/2):
                            position_x_pacman = int(largeur_obstacle*(position_x_pacman//largeur_obstacle)+int(largeur_obstacle/2))
                            direction_pacman = memorisation_direction


        if memorisation_direction == 2:
            if direction_pacman==1:
                direction_pacman=2
            else:
                if direction_pacman == 3 or direction_pacman == 4:
                    if grille_jeu[y_pacman_grille+1][x_pacman_grille] != 1:
                        if position_x_pacman%largeur_obstacle>=int(largeur_obstacle/2) and (position_x_pacman-vitesse)%largeur_obstacle<=int(largeur_obstacle/2):
                            position_x_pacman = int(largeur_obstacle*(position_x_pacman//largeur_obstacle)+int(largeur_obstacle/2))
                            direction_pacman = memorisation_direction


        if memorisation_direction == 3:
            if direction_pacman==4:
                direction_pacman=3
            else:
                if direction_pacman == 1 or direction_pacman ==2 :
                    if grille_jeu[y_pacman_grille][x_pacman_grille-1] != 1:
                        if position_y_pacman%hauteur_obstacle<=int(hauteur_obstacle/2) and (position_y_pacman+vitesse)%hauteur_obstacle>=int(hauteur_obstacle/2):
                            position_x_pacman = int(largeur_obstacle*(position_x_pacman//largeur_obstacle)+int(largeur_obstacle/2))
                            direction_pacman = memorisation_direction


        if memorisation_direction == 4:
            if direction_pacman==3:
                direction_pacman=4
            else:
                if direction_pacman == 1 or direction_pacman == 2:
                    if grille_jeu[y_pacman_grille][x_pacman_grille+1] != 1:
                        if position_y_pacman%hauteur_obstacle<=int(hauteur_obstacle/2) and (position_y_pacman+vitesse)%hauteur_obstacle>=int(hauteur_obstacle/2):
                            position_x_pacman = int(largeur_obstacle*(position_x_pacman//largeur_obstacle)+int(largeur_obstacle/2))
                            direction_pacman = memorisation_direction






        if direction_pacman == 1:
            if grille_jeu[y_pacman_grille-1][x_pacman_grille] != 1:
                position_y_pacman -= vitesse
            elif position_y_pacman%hauteur_obstacle>int(hauteur_obstacle/2):
                if (position_y_pacman-vitesse)%hauteur_obstacle<int(hauteur_obstacle/2):
                    position_y_pacman = y_pacman_grille*hauteur_obstacle+int(hauteur_obstacle/2)
                else:
                    position_y_pacman -= vitesse

        if direction_pacman == 2:
            if grille_jeu[y_pacman_grille+1][x_pacman_grille] != 1:
                position_y_pacman += vitesse
            elif position_y_pacman%hauteur_obstacle<int(hauteur_obstacle/2):
                if (position_y_pacman+vitesse)%hauteur_obstacle>int(hauteur_obstacle/2):
                    position_y_pacman = y_pacman_grille*hauteur_obstacle+int(hauteur_obstacle/2)
                else:
                    position_y_pacman += vitesse

        if direction_pacman == 3:
            if grille_jeu[y_pacman_grille][x_pacman_grille-1] != 1:
                position_x_pacman -= vitesse
            elif position_x_pacman%largeur_obstacle>int(hauteur_obstacle/2):
                if (position_x_pacman-vitesse)%largeur_obstacle<int(hauteur_obstacle/2):
                    position_x_pacman = x_pacman_grille*largeur_obstacle+int(largeur_obstacle/2)
                else:
                    position_x_pacman -= vitesse

        if direction_pacman == 4:
            if grille_jeu[y_pacman_grille][x_pacman_grille+1] != 1:
                position_x_pacman += vitesse
            elif position_x_pacman%largeur_obstacle<int(hauteur_obstacle/2):
                if (position_x_pacman+vitesse)%largeur_obstacle>int(hauteur_obstacle/2):
                    position_x_pacman = x_pacman_grille*largeur_obstacle+int(largeur_obstacle/2)
                else:
                    position_x_pacman += vitesse


        x_pacman_grille = int(position_x_pacman/largeur_obstacle)
        y_pacman_grille = int(position_y_pacman/hauteur_obstacle)
        return position_x_pacman, position_y_pacman, direction_pacman, x_pacman_grille, y_pacman_grille


    #----INITIALISATION DE LA GRILLE DE JEU----
    f = open('map.txt','r')
    l = f.read().split("\n")
    l2 = l[0].split(",")
    largeur_grille = int(l2[0])
    hauteur_grille = int(l2[1])

    grille_jeu = [None]*hauteur_grille
    for i in range(hauteur_grille):
        grille_jeu[i] = [None]*largeur_grille

    for x in range(largeur_grille):
        for y in range(hauteur_grille):
            if l[1+y][x]=="#":
                grille_jeu[y][x] = 1
            elif l[1+y][x]=="O":
                grille_jeu[y][x] = 2
                if coordonnees_portail_1 == (0,0):#Si les coordonnees du 1er portail ne sont pas connues, on les enregistre
                    coordonnees_portail_1 = (x,y)
                else:#On connait deja le premier portail, on enregistre le 2eme
                    coordonnees_portail_2 = (x,y)
            else:
                grille_jeu[y][x] = 0
    hauteur_obstacle =height/hauteur_grille
    largeur_obstacle = width/largeur_grille

    #x_bonus, y_bonus = generer_bonus() géré côté serveur
    #info_a_envoyer = bytes(f"bonus {x_bonus} {y_bonus}", "utf-8")
    #----FIN INITIALISATION GRILLE DE JEU----


    running = True

    while running and not died:
        if time.time()-derniere_actualisation_image>1.0/fps:
            derniere_actualisation_image = time.time()
            x_fantome, y_fantome, x_grille_fantome, y_grille_fantome = coordonnees_fantome()
            position_x_pacman, position_y_pacman, direction_pacman, x_pacman_grille, y_pacman_grille = update_position(position_x_pacman, position_y_pacman, direction_pacman)
            update_screen()

            if (x_pacman_grille, y_pacman_grille)==coordonnees_portail_1 and time.time()-derniere_teleportation_portail>cooldown_portail:#Téléportation avec le premier portail
                print("Teleportation portail 1")
                position_x_pacman = int(coordonnees_portail_2[0]*largeur_obstacle + int(largeur_obstacle/2))
                position_y_pacman = int(coordonnees_portail_2[1]*hauteur_obstacle + int(largeur_obstacle/2))
                derniere_teleportation_portail = time.time()
            if (x_pacman_grille, y_pacman_grille)==coordonnees_portail_2 and time.time()-derniere_teleportation_portail>cooldown_portail:#Téléportation avec le premier portail
                print("Teleportation portail 2")
                position_x_pacman = int(coordonnees_portail_1[0]*largeur_obstacle + int(largeur_obstacle/2))
                position_y_pacman = int(coordonnees_portail_1[1]*hauteur_obstacle + int(largeur_obstacle/2))
                derniere_teleportation_portail = time.time()
            if bonus_sur_le_jeu and distance(position_x_pacman, position_y_pacman, x_bonus, y_bonus)<1.25*rayon_pacman:
                pacman_power_up = True
                vitesse = 4
                heure_consommation_bonus = time.time()
                bonus_sur_le_jeu = False#On affiche plus le bonus
                info_a_envoyer = bytes(f"bonus mange", "utf-8")
                #Envoyer au fantome qu'on a mangé le bonus
            if pacman_power_up and time.time()-heure_consommation_bonus>temps_bonus:
                pacman_power_up = False
                vitesse = 3
                info_a_envoyer = bytes(f"powerup fin", "utf-8")
                #Envoyer au fantome qu'on a terminé le bonus
            '''if time.time()-heure_consommation_bonus>temps_avant_reapparition_bonus and not bonus_sur_le_jeu:
                x_bonus, y_bonus = generer_bonus()
                info_a_envoyer = bytes(f"bonus {x_bonus} {y_bonus}", "utf-8")
                bonus_sur_le_jeu = True''' #le bonus est généré côté serveur
            if len(donneesJoueurs) > 1 and donneesJoueurs[1] != None:
                x_bonus, y_bonus = donneesJoueurs[1]
                bonus_sur_le_jeu = True

            if len(donneesJoueurs)>0:
                #print(donneesJoueurs)
                dic = donneesJoueurs[0]
                for key in dic.keys():
                    if dic[key]['pacman'] == False:#Le perso est un fantome
                        try:
                            x, y = tuple(dic[key]['pos'].split(" "))
                            x , y= int(x), int(y)
                            if distance(x, y, position_x_pacman, position_y_pacman)<2*rayon_pacman:
                                if not pacman_power_up:
                                    died = True
                                    print("Vous avez été mangé par un fantome...")
                                    info_a_envoyer = bytes(f"died {nomJoueur}", "utf-8")
                                else:#on est en powerup
                                    print("Vous avez tué un fantome !")
                                    info_a_envoyer = bytes(f"died {key}", "utf-8")
                        except:
                            pass


            '''if died: #désactivé suite à modification systeme mort
                running = False
                if pacman_power_up:
                    print("Vous avez mangé le fantome ! Félcitations")
                else:
                    print("Vous avez été mangé par le fantome...")
                await asyncio.sleep(0.2)'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    memorisation_direction = 3
                if event.key == pygame.K_RIGHT:
                    memorisation_direction = 4
                if event.key == pygame.K_UP:
                    memorisation_direction = 1
                if event.key == pygame.K_DOWN:
                    memorisation_direction = 2
                    #position_x_pacman += 1
        await asyncio.sleep(0.001)


    pygame.quit()


async def communication():
    global x_fantome, y_fantome, position_x_pacman, position_y_pacman, derniere_actualisation_image, died, info_a_envoyer, donneesJoueurs, nomJoueur
    import socket, asyncio
    hote = "127.0.0.1"
    port = 25565
    x_fantome, y_fantome = 789, 456

    loop = asyncio.get_event_loop()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setblocking(False)

    await loop.sock_connect(socket, (hote, port))
    print(f"Connection on {port}")
    await loop.sock_sendall(socket, b"moi pacman")
    nomJoueur = await loop.sock_recv(socket, 255)
    print(f"Vous êtes le joueur {nomJoueur.decode('utf-8')}")
    await asyncio.sleep(0.1)

    while derniere_actualisation_image > time.time() - 1:
        if not died:
            if info_a_envoyer == None:
                await loop.sock_sendall(socket, bytes("pos " + str(position_x_pacman) + " " + str(position_y_pacman), "utf-8"))
            else:
                await loop.sock_sendall(socket, info_a_envoyer)
                info_a_envoyer = None
            var = await loop.sock_recv(socket, 1024)
            #print(var)
            if var == b"died":
                died = True
                print("Vous avez été mangé par un fantôme !")
            else:
                var = await get_var_from_json(var)
                donneesJoueurs = var

        await asyncio.sleep(refreshTime)

    print("Close")
    await loop.sock_sendall(socket, bytes("close", 'utf-8'))
    socket.close()

async def get_var_from_bstr(bstr: bytes):
    bstr = bstr.decode("utf-8")
    r = []
    for v in bstr.split():
        r.append(int(float(v)))
    return r

async def get_var_from_json(bstr: bytes):
    bstr = bstr.decode("utf-8")
    return json.loads(bstr)



async def main():
    #derniere_actualisation_image = time.time()
    global x_fantome, y_fantome, position_x_pacman, position_y_pacman, derniere_actualisation_image, info_a_envoyer, nomJoueur, donneesJoueurs
    nomJoueur = None
    donneesJoueurs = {}
    info_a_envoyer = None
    loop = asyncio.get_event_loop()
    task_gui = loop.create_task(gui())
    task_communication = loop.create_task(communication())
    await task_communication
    await task_gui


refreshTime = 0.002
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
