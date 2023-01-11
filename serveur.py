import socket

# -------------- Constantes --------------
HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 4000

# --------------- Fonctions ---------------
def send(data):
    connection_socket.sendall(data.encode('ascii', errors='ignore'))
    
def shell_serveur():
    while True:
        
        command = input("shell: " + listen() + " > ")
        
        if command == "exit":
            return
        
        send(command)
        print(listen())

def socket_receive_all_data(socket_p, data_len):
	current_data_len = 0
	total_data = None
	print("socket_receive_data_len:", data_len)
	while current_data_len < data_len:
		chunk_len = data_len - current_data_len
		if chunk_len > MAX_DATA_SIZE:
			chunk_len = MAX_DATA_SIZE
		data = socket_p.recv(chunk_len)
		print("	len:", len(data))
		if not data:
			return None
		if not total_data:
			total_data = data
		else:
			total_data += data
		current_data_len += len(data)
		print("	total len:", current_data_len, "/", data_len)
	return total_data



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

	header_data = socket_receive_all_data(connection_socket, 13)
	longeur_data = int(header_data.decode('ascii', errors='ignore'))
	data_recues = socket_receive_all_data(connection_socket, longeur_data)







	if command == "shell":
		send(command)
		shell_serveur()
	
	print(listen())

	

connection_socket.close()


