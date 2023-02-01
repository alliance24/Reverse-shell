import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 3500
MAX_DATA_SIZE = 1024

def recive():
    data = s.recv(MAX_DATA_SIZE)
    return data
    
def send(data):
    # data = data.encode('ascii', errors='ignore')
    s.sendall(data.encode('ascii', errors='ignore'))
    
def send_and_recive(data):
    send(data)
    reponse = recive()
    return reponse

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_adress = s.accept()
print(f"Connexion établie avec {client_adress}")

while True:
    commande = input(client_adress[0] + ":" + str(client_adress[1]) + 
                     " " + send_and_recive("command_infos").decode('ascii', errors='ignore') + " > ")