import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 1024

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_adress = s.accept()
print(f"Connexion établie avec {client_adress}")

while True:
	commande = input("Commande: ")
	connection_socket.sendall(commande.encode())
	data_recues = connection_socket.recv(MAX_DATA_SIZE)
	if commande == "shell":
		while data_recues != "exit":
			text = "os.getcwd"
			connection_socket.sendall(commande.encode())
			get_dir = connection_socket.recv(MAX_DATA_SIZE)
			commande = input(get_dir + " > ")

	# data_recues = connection_socket.recv(MAX_DATA_SIZE)
	# if not data_recues:
	# 	break
	# print(data_recues.decode())

s.close()
connection_socket.close()


