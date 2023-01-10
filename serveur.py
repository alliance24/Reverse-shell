import socket

HOST_IP = "127.0.0.1"
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

while True:
	command = input("Commande: ")
	command_split = command.split(" ")

	
	if command == "":
		continue
	if command == "shell":
		send(command)
		shell_serveur()
	
	print(listen())

	
  
  
  
  
  
  
	# else:
	# 	C.sendall(command.encode())
	# data_recues = connection_socket.recv(MAX_DATA_SIZE)
	# if commande == "shell":
	# 	while data_recues != "exit":
	# 		text = "os.getcwd"
	# 		connection_socket.sendall(commande.encode())
	# 		get_dir = connection_socket.recv(MAX_DATA_SIZE)
	# 		commande = input(get_dir + " > ")
	# data_recues = connection_socket.recv(MAX_DATA_SIZE)
	# if not data_recues:
	# 	break
	# print(data_recues.decode())

connection_socket.close()


