import socket, asyncio
import time, json

port = 25565
socket_var = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_var.bind(('', port))

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
				dernierNombre += 1
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
		elif receivedSplitted[0] == b"powerup_eaten":
			donneesJoueurs[nomJoueur]["powerup_on"] = True
			posPowerup = None
		elif receivedSplitted[0] == b"powerup_ended":
			donneesJoueurs[nomJoueur]["powerup_on"] = False
		elif receivedSplitted[0] == b"died":
			donneesJoueurs.pop(nomJoueur)
			listeJoueurs.remove(nomJoueur)
			running = False
		elif receivedSplitted[0] == b"close":
			running = False
			listeJoueurs.remove(nomJoueur)
			donneesJoueurs.pop(nomJoueur)
		else:
			print(f"Recu d'un client inconnu : {received}")
		
		if running:
			print(donneesJoueurs)
			await loop.sock_sendall(client, bytes(json.dumps([donneesJoueurs, posPowerup]), "utf-8"))
			
		'''if pacman:
            received = await loop.sock_recv(client, 255)
            if received == b"close":
                running = False

            else:
                if received.split()[0] != b"posPac":
                    info_a_envoyer_a_fantome = received
                else:
                    posPacman = received

                if info_a_envoyer_a_pacman != None:
                    await loop.sock_sendall(client, info_a_envoyer_a_pacman)
                    info_a_envoyer_a_pacman = None
                else:
                    await loop.sock_sendall(client, posFantome)
        else:
            received = await loop.sock_recv(client, 20)
            if received == b"close":
                running = False

            else:
                if received.split()[0] != b"posFan":
                    info_a_envoyer_a_pacman = received
                else:
                    posFantome = received

                if info_a_envoyer_a_fantome != None:
                    await loop.sock_sendall(client, info_a_envoyer_a_fantome)
                    info_a_envoyer_a_fantome = None
                else:
                    await loop.sock_sendall(client, posPacman)'''
	print("connection closed")


async def main():
	global donneesJoueurs, listeJoueurs, posPowerup
	donneesJoueurs = {}
	listeJoueurs = []
	posPowerup = None #les coords sous la forme b"pos_x pos_y"

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