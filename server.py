import socket, asyncio
import time

port = 25565
socket_var = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_var.bind(('', port))

async def gerer_connexion(client, loop):
    global posPacman, posFantome, last_game_end, info_a_envoyer_a_fantome, info_a_envoyer_a_pacman
    response = await loop.sock_recv(client, 512)
    pacman = None
    if response == b"moi pacman":
        pacman = True
        print("pacman initialisé")
    elif response == b"moi fantome":
        pacman = False
        print("fantôme initialisé")
    else:
        print(response)
        print("Erreur initialisation fantome/pacman")
    #last20 = time.time()
    #counter = 0
    running = True
    while running:
        await asyncio.sleep(0.005)
        if pacman:
            received = await loop.sock_recv(client, 20)
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
                    await loop.sock_sendall(client, posPacman)
    print("connection closed")
    last_game_end = time.time()


async def main():
    global posPacman, posFantome, last_game_end, info_a_envoyer_a_fantome, info_a_envoyer_a_pacman

    last_game_end = time.time()
    info_a_envoyer_a_fantome, info_a_envoyer_a_pacman = None, None
    posPacman, posFantome = b"posPac 540 360", b"posFan 789 456"
    print(f"Ecoute sur le port {port}...")
    socket_var.listen(10)  # le nombre max de connections
    socket_var.setblocking(False)
    loop = asyncio.get_event_loop()
    while True:
        try:
            client, address = await loop.sock_accept(socket_var)
            print(f"{address} connected")
            if last_game_end < time.time() - 5:
                posPacman, posFantome = b"posPac 540 360", b"posFan 789 456"
                info_a_envoyer_a_fantome, info_a_envoyer_a_pacman = None, None
            asyncio.create_task(gerer_connexion(client, loop))
        except:
            print("Connection lost")
    print("Closing server")
    client.close()
    socket.close()

asyncio.run(main())