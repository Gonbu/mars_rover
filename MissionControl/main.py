import socket
import pickle
import threading
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from MissionControl.missionControlRunner import MissionControlRunner
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.MissionRover.command import Command
from Domain.Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
from SocketCommunication.ReceiverFromRover import ReceiverFromRover
from SocketCommunication.SenderToRover import SenderToRover
from Missions.marsMission import *

def initialize_server_address():
    # Définition de l'adresse IP et du port du serveur auquel se connecter
    valid_server_address_input = False
    while not valid_server_address_input:
        server_address_input = input('Voulez-vous utiliser le répéteur ? (O/N) : ').replace(" ", "")
        if server_address_input == "O":
            return repeater_address
        elif server_address_input == "N":
            return rover_address

def main() :
    # Initialisation des objets de communication
    sender = SenderToRover()
    receiver = ReceiverFromRover()
    protocol = MyCommunicationProtocol(sender, receiver)

    # Établissement de la connexion avec le serveur
    server_address = initialize_server_address()
    protocol.establish_connection(server_address)

    # Initialisation du rover
    rover = Rover(position_x_start, position_y_start, orientation_start)

    # Création de l'instance MissionControlRunner
    mission_control_runner = MissionControlRunner(sender, receiver, protocol, rover, server_address)

    # Exécutez la logique du mission control
    mission_control_runner.run_from_mission_control()

if __name__ == "__main__":
    main()
