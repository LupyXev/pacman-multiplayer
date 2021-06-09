import socket, asyncio
import json, random

port = 25565
socket_var = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_var.bind(('', port))


#----INITIALISATION DE LA GRILLE DE JEU----
width,height = 1080,720
coordonnees_portail_1 = (0,0) #Coordonnées dans la grille de jeu du 1er portail
coordonnees_portail_2 = (0,0)
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

async def generer_bonus():#Fonction pour générer une position pour le bonus
	x_grille_bonus = 0
	y_grille_bonus = 0
	while grille_jeu[y_grille_bonus][x_grille_bonus] == 1:#On recalcule des coordonnees jusqu'à tomber dans une case vide
		x_grille_bonus = random.randint(0,largeur_grille-1)
		y_grille_bonus = random.randint(0,hauteur_grille-1)
	x_bonus = largeur_obstacle*x_grille_bonus+(largeur_obstacle/2)
	y_bonus = hauteur_obstacle*y_grille_bonus+(hauteur_obstacle/2)
	return [x_bonus, y_bonus]

async def gerer_connexion(client, loop):
	global donneesJoueurs, listeJoueurs, posPowerup
	#global posPacman, posFantome, last_game_end, info_a_envoyer_a_fantome, info_a_envoyer_a_pacman
	response = await loop.sock_recv(client, 255)
	pacman = None
	type = None
	dernierNombre = 0
	if response == b"moi pacman":
		pacman = True
		print("pacman initialisé")
		type = 1
	elif response == b"moi fantome":
		pacman = False
		print("fantôme initialisé")
		type = 0
	else:
		print(response)
		print("Erreur initialisation fantome/pacman")
	for p in listeJoueurs:
			if p >= dernierNombre:
				dernierNombre = p + 1
	#last20 = time.time()
	#counter = 0
	if pacman:
		nomJoueur = dernierNombre
	else:
		nomJoueur = dernierNombre
		
	await loop.sock_sendall(client, bytes(str(nomJoueur), "utf-8"))
	listeJoueurs.append(nomJoueur)
	donneesJoueurs[nomJoueur] = {"pos": "", "powerup_on": False, "pacman": pacman}
	running = True
	while running:
		await asyncio.sleep(0.004)
		received = await loop.sock_recv(client, 255)
		receivedSplitted = received.split()
		if nomJoueur not in donneesJoueurs:
			running = False
			await loop.sock_sendall(client, bytes("died", "utf-8"))
		elif receivedSplitted[0] == b"pos":
			donneesJoueurs[nomJoueur]["pos"] = received[4:].decode("utf-8")
		elif received == b"bonus mange":
			donneesJoueurs[nomJoueur]["powerup_on"] = True
			posPowerup = await generer_bonus()
		elif received == b"powerup fin":
			donneesJoueurs[nomJoueur]["powerup_on"] = False
		elif receivedSplitted[0] == b"died":
			try:
				donneesJoueurs.pop(int(receivedSplitted[1].decode("utf-8")))
				listeJoueurs.remove(int(receivedSplitted[1].decode("utf-8")))
				print(f"suppression réussite du joueur {int(receivedSplitted[1].decode('utf-8'))}")
			except:
				pass
		elif receivedSplitted[0] == b"close":
			running = False
			listeJoueurs.remove(nomJoueur)
			donneesJoueurs.pop(nomJoueur)
		else:
			print(f"Erreur : Recu d'un client inconnu : {received}")
		
		if running:
			#print(donneesJoueurs)
			await loop.sock_sendall(client, bytes(json.dumps([donneesJoueurs, posPowerup]), "utf-8"))
			

	print(f"connection closed (joueur {nomJoueur})")


async def main():
	global donneesJoueurs, listeJoueurs, posPowerup
	donneesJoueurs = {}
	listeJoueurs = []
	posPowerup = await generer_bonus() #les coords sous la forme [pos_x pos_y]

	#info_a_envoyer_a_fantome, info_a_envoyer_a_pacman = None, None
	#posPacman, posFantome = b"posPac 540 360", b"posFan 789 456"
	print(f"Ecoute sur le port {port}...")
	socket_var.listen(35)  # le nombre max de connections
	socket_var.setblocking(False)
	loop = asyncio.get_event_loop()
	while True:
		try:
			client, address = await loop.sock_accept(socket_var)
			print(f"{address} connected")
			asyncio.create_task(gerer_connexion(client, loop))
		except:
			print("Connection lost")
	print("Closing server")
	client.close()
	socket.close()

asyncio.run(main())