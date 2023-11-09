import socket
import pickle
import threading
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.MissionRover.instruction import Instruction
from Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from Communication.ProtocolCommunication import MyCommunicationProtocol
from Domain.MissionRover.missionInitializer import *

class MyCommandSender(CommandSender):
    def send_command(self, instructions):
        data_to_send = protocol.encode(instructions)
        protocol.client_socket.sendall(data_to_send)

class MyCommandReceiver(CommandReceiver):
    def receive_command(self):
        # Réception de la longueur des données en tant que préfixe
        data_length_bytes = protocol.client_socket.recv(4)
        data_length = int.from_bytes(data_length_bytes, byteorder='big')

        # Réception des données
        data = b""
        while len(data) < data_length:
            chunk = protocol.client_socket.recv(data_length - len(data))
            if not chunk:
                raise Exception("Connexion interrompue avant la fin de la réception des données.")
            data += chunk

        # Décodage des données
        decoded_data = data.decode('utf-8')
        rover_str, coords = decoded_data.split(',')[0:3], list(map(int, decoded_data.split(',')[3:]))
        rover.from_repr(rover_str)
        return rover, coords

# Définition de l'adresse IP et du port du serveur auquel se connecter
valid_server_address_input = False
while not valid_server_address_input:
    server_address_input = input('Voulez-vous utiliser le répéteur ? (O/N) : ').replace(" ", "")
    if server_address_input == "O":
        server_address = ('127.0.0.1', 12346)
        valid_server_address_input = True
    elif server_address_input == "N":
        server_address = ('127.0.0.1', 12345)
        valid_server_address_input = True

# Initialisation des objets de communication
sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol = MyCommunicationProtocol(sender, receiver)

# Établissement de la connexion avec le serveur
protocol.establish_connection(server_address)

# Initialisation du rover
rover = Rover(position_x_start, position_y_start, orientation_start)

while True:
    # Collecte des instructions
    instructions = Instruction()
    instructions.add_instruction()

    # Envoi des commandes au rover
    sender.send_command(instructions._Instruction__instruction_order)

    # Réception de l'état mis à jour du rover
    rover, obstacle = receiver.receive_command()

    # Traitement des données reçues du rover
    rover.to_string()
    if len(obstacle) > 0:
        print("Obstacle : {}".format(obstacle))

# Fermeture du socket client (Note : il manquait l'initialisation du socket client dans votre code)
protocol.client_socket.close()
