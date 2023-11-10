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
from Domain.Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
from SocketCommunication.CommandReceiverRover import CommandReceiverRover
from SocketCommunication.CommandSenderRover import CommandSenderRover
from Missions.marsMission import *

def initialize_server_address():
    # Définition de l'adresse IP et du port du serveur auquel se connecter
    valid_server_address_input = False
    while not valid_server_address_input:
        server_address_input = input('Voulez-vous utiliser le répéteur ? (O/N) : ').replace(" ", "")
        if server_address_input == "O":
            return ('127.0.0.1', 12346)
        elif server_address_input == "N":
            return ('127.0.0.1', 12345)

def main() :
    # Initialisation des objets de communication
    sender = CommandSenderRover()
    receiver = CommandReceiverRover()
    protocol = MyCommunicationProtocol(sender, receiver)

    # Établissement de la connexion avec le serveur
    server_address = initialize_server_address()
    protocol.establish_connection(server_address)

    # Initialisation du rover
    rover = Rover(position_x_start, position_y_start, orientation_start)

    try :
        while True:
            # Collecte des instructions
            instructions = Instruction()
            instructions.add_instruction()

            # Envoi des commandes au rover
            sender.send_command(protocol, instructions._Instruction__instruction_order)

            # Réception de l'état mis à jour du rover
            rover, obstacle = receiver.receive_command(protocol, rover)

            # Traitement des données reçues du rover
            rover.to_string()
            if len(obstacle) > 0:
                print("Obstacle : {}".format(obstacle))
    finally :
        # Fermeture du socket client (Note : il manquait l'initialisation du socket client dans votre code)
        protocol.client_socket.close()



if __name__ == "__main__":
    main()
