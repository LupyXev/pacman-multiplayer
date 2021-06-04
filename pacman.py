import pygame
import time
import math
import asyncio
async def gui():
    global x_fantome, y_fantome, position_x_pacman, position_y_pacman

    width,height = 1080,720
    screen = pygame.display.set_mode((width,height),0,8)

    position_x_pacman = int(width/2)
    position_y_pacman = int(height/2)
    x_pacman_grille = 0
    y_pacman_grille = 0
    x_fantome = 0
    y_fantome = 0
    x_grille_fantome = 0
    y_grille_fantome = 0
    rayon_pacman = 31
    vitesse = 4

    direction_pacman = 0#Direction dans laquelle va pacman : 0 immobile, 1 haut, 2 bas, 3 gauche, 4 droite
    memorisation_direction = 0#Future direction où va aller pacman, quand il le pourra

    def distance(x1,y1,x2,y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    def coordonnees_fantome():
        #x_fantome, y_fantome sont récupérés par communication()
        x_grille_fantome, y_grille_fantome = int(x_fantome/largeur_obstacle), int(y_fantome/hauteur_obstacle)
        return x_fantome, y_fantome, x_grille_fantome, y_grille_fantome

    def update_screen():
        screen.fill((0,0,100))

        #Mise à jour de la grille

        for y in range(hauteur_grille):
            for x in range(largeur_grille):
                if grille_jeu[y][x] == 1:
                    niveau_rouge = int(abs(x**3-y**3)/14)
                    #print(niveau_rouge)
                    pygame.draw.rect(screen, (255,0,0), (x*largeur_obstacle, y*hauteur_obstacle, largeur_obstacle, hauteur_obstacle))


        pygame.draw.circle(screen, (255,255,0), (position_x_pacman, position_y_pacman), rayon_pacman)

        pygame.draw.circle(screen, (0,0,0), (position_x_pacman+int(rayon_pacman/2), position_y_pacman-int(rayon_pacman/2)), int(rayon_pacman/5))
        pygame.draw.line(screen, (0,0,0), (position_x_pacman+int(rayon_pacman/4), position_y_pacman),( position_x_pacman+rayon_pacman, position_y_pacman))
        pygame.draw.circle(screen, (255,255,255), (x_fantome, y_fantome), rayon_pacman)
        pygame.display.flip()

    def update_position(position_x_pacman, position_y_pacman, direction_pacman):

        if memorisation_direction == 1:
            x_pacman_grille = int(position_x_pacman/largeur_obstacle)
            y_pacman_grille = int((position_y_pacman-vitesse-rayon_pacman)/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                if direction_pacman == 3:#Pour éviter d'être à moitié dans un mur
                    x_pacman_grille = int((position_x_pacman+rayon_pacman)/largeur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 1
                elif direction_pacman == 4:#Pour éviter d'être à moitié dans un mur
                    x_pacman_grille = int((position_x_pacman-rayon_pacman)/largeur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 1
                else:
                    direction_pacman = 1

        elif memorisation_direction == 2:
            x_pacman_grille = int(position_x_pacman/largeur_obstacle)
            y_pacman_grille = int((position_y_pacman+vitesse+rayon_pacman)/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                if direction_pacman == 3:#Pour éviter d'être à moitié dans un mur
                    x_pacman_grille = int((position_x_pacman+rayon_pacman)/largeur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 2
                elif direction_pacman == 4:#Pour éviter d'être à moitié dans un mur
                    x_pacman_grille = int((position_x_pacman-rayon_pacman)/largeur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 2
                else:
                    direction_pacman = 2

        elif memorisation_direction == 3:
            x_pacman_grille = int((position_x_pacman-vitesse-rayon_pacman)/largeur_obstacle)
            y_pacman_grille = int(position_y_pacman/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                if direction_pacman == 2:#Pour éviter d'être à moitié dans un mur
                    y_pacman_grille = int((position_y_pacman-rayon_pacman)/hauteur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 3
                elif direction_pacman == 1:#Pour éviter d'être à moitié dans un mur
                    y_pacman_grille = int((position_y_pacman+rayon_pacman)/hauteur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 3
                else:
                    direction_pacman = 3

        elif memorisation_direction == 4:
            x_pacman_grille = int((position_x_pacman+vitesse+rayon_pacman)/largeur_obstacle)
            y_pacman_grille = int(position_y_pacman/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                if direction_pacman == 2:#Pour éviter d'être à moitié dans un mur
                    y_pacman_grille = int((position_y_pacman-rayon_pacman)/hauteur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 4
                elif direction_pacman == 1:#Pour éviter d'être à moitié dans un mur
                    y_pacman_grille = int((position_y_pacman+rayon_pacman)/hauteur_obstacle)
                    if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                        direction_pacman = 4
                else:
                    direction_pacman = 4



        if direction_pacman == 1:
            x_pacman_grille = int(position_x_pacman/largeur_obstacle)
            y_pacman_grille = int((position_y_pacman-vitesse-rayon_pacman)/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                position_y_pacman -= vitesse
        elif direction_pacman == 2:
            x_pacman_grille = int(position_x_pacman/largeur_obstacle)
            y_pacman_grille = int((position_y_pacman+vitesse+rayon_pacman)/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                position_y_pacman += vitesse
        elif direction_pacman == 3:
            x_pacman_grille = int((position_x_pacman-vitesse-rayon_pacman)/largeur_obstacle)
            y_pacman_grille = int(position_y_pacman/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                position_x_pacman -= vitesse
        elif direction_pacman == 4:
            x_pacman_grille = int((position_x_pacman+vitesse+rayon_pacman)/largeur_obstacle)
            y_pacman_grille = int(position_y_pacman/hauteur_obstacle)
            if grille_jeu[y_pacman_grille][x_pacman_grille] != 1:
                position_x_pacman += vitesse
        x_pacman_grille = int(position_x_pacman/largeur_obstacle)
        y_pacman_grille = int((position_y_pacman-vitesse-rayon_pacman)/hauteur_obstacle)
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
            else:
                grille_jeu[y][x] = 0
    hauteur_obstacle =height/hauteur_grille
    largeur_obstacle = width/largeur_grille
    #----FIN INITIALISATION GRILLE DE JEU----


    running = True

    while running:
        await asyncio.sleep(refreshTime)
        #print(data)
        x_fantome, y_fantome, x_grille_fantome, y_grille_fantome = coordonnees_fantome()
        position_x_pacman, position_y_pacman, direction_pacman, x_pacman_grille, y_pacman_grille = update_position(position_x_pacman, position_y_pacman, direction_pacman)
        update_screen()
        if distance(position_x_pacman, position_y_pacman, x_fantome, y_fantome)<2*rayon_pacman:
            running = False
            print("Pacman est mort :(")
            await asyncio.sleep(0.2)
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


    pygame.quit()



async def communication():
    global x_fantome, y_fantome, position_x_pacman, position_y_pacman
    import socket, asyncio
    hote = "127.0.0.1"
    port = 1919
    x_fantome, y_fantome = 789, 456

    loop = asyncio.get_event_loop()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setblocking(False)

    await loop.sock_connect(socket, (hote, port))
    print(f"Connection on {port}")
    await loop.sock_sendall(socket, b"moi pacman")
    await asyncio.sleep(refreshTime*2)
    while True:
        await loop.sock_sendall(socket, bytes(str(position_x_pacman) + " " + str(position_y_pacman), "utf-8"))
        var = await loop.sock_recv(socket, 20)
        x_fantome, y_fantome = await get_var_from_bstr(var)
        await asyncio.sleep(refreshTime/2)

    print("Close")
    socket.close()

async def get_var_from_bstr(bstr: bytes):
    bstr = bstr.decode("utf-8")
    r = []
    for v in bstr.split():
        r.append(int(v))
    return r


async def main():
    global x_fantome, y_fantome, position_x_pacman, position_y_pacman
    data = None
    task_gui = asyncio.create_task(gui())
    task_communication = asyncio.create_task(communication())
    await task_communication
    await task_gui


refreshTime = 0.02
asyncio.run(main())