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
    def send_command(self, instructions):
        serialized_instructions = pickle.dumps(instructions)
        protocol_sender.client_socket.send(serialized_instructions)

class MyCommandReceiver(CommandReceiver):
    def receive_command(self):
        data = protocol_reciver.client_socket.recv(1024)
        command_obj = pickle.loads(data)
        return command_obj

# Définit l'adresse IP et le port du Rover auquel se connecter
rover_address = ('127.0.0.1', 12345)
server_address = ('127.0.0.1', 12346)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol_reciver = MyCommunicationProtocol(sender, receiver)
protocol_sender = MyCommunicationProtocol(sender, receiver)
    
# Initialise le serveur sur server_address
protocol_reciver.initialize_server(server_address)
# Établir la connexion avec le Rover
protocol_sender.establish_connection(rover_address)



# Le Repeater agit en tant que relais entre MissionControl et Rover
while True:
    instructions = receiver.receive_command()
    if not instructions:
        break  # Fin de la communication
    # Réexpédier les instructions au Rover
    sender.send_command(instructions)

# Ferme le socket client
protocol_reciver.close_connection()
protocol_sender.close_connection()
