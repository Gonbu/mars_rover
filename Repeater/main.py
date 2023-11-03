import socket
import pickle
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from Communication.ProtocolCommunication import MyCommunicationProtocol

class MyCommandSender(CommandSender):
    def send_command(self, data, protocol):
        serialized_data = pickle.dumps(data)
        data_length = len(serialized_data).to_bytes(4, byteorder='big')
        data_to_send = data_length + serialized_data
        protocol.client_socket.sendall(data_to_send)

class MyCommandReceiver(CommandReceiver):
    def receive_command(self, protocol):
        data_length_bytes = protocol.client_socket.recv(4)
        data_length = int.from_bytes(data_length_bytes, byteorder='big')
        data = b""
        while len(data) < data_length:
            chunk = protocol.client_socket.recv(data_length - len(data))
            if not chunk:
                raise Exception("Connexion interrompue avant la fin de la réception des données.")
            data += chunk
        decoded_data = pickle.loads(data)
        return decoded_data

# Définit l'adresse IP et le port du Rover auquel se connecter
rover_address = ('127.0.0.1', 12345)
server_address = ('127.0.0.1', 12346)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol_server = MyCommunicationProtocol(sender, receiver)
protocol_client = MyCommunicationProtocol(sender, receiver)
    
# Initialise le serveur sur server_address
protocol_server.initialize_server(server_address)
# Établir la connexion avec le Rover
protocol_client.establish_connection(rover_address)

# Le Repeater agit en tant que relais entre MissionControl et Rover
while True:
    data = receiver.receive_command(protocol_server)
    if not data:
        break  # Fin de la communication

    # Réexpédier les données à Rover
    sender.send_command(data, protocol_client)

    # Recevoir les données de Rover
    received_data = receiver.receive_command(protocol_client)

    # Réexpédier les données à MissionControl
    sender.send_command(received_data, protocol_server)

# Ferme les sockets
protocol_server.close_connection()
protocol_client.close_connection()
