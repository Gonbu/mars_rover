import socket
import pickle
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.rover import Rover
from Domain.MissionRover.command import Command
from Domain.Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
from SocketCommunication.ReceiverFromRover import ReceiverFromRover
from SocketCommunication.SenderToRover import SenderToRover
from SocketCommunication.ReceiverFromMissionControl import ReceiverFromMissionControl
from SocketCommunication.SenderToMissionControl import SenderToMissionControl
from Missions.marsMission import *

def main() :
    # Définit l'adresse IP et le port du Rover auquel se connecter

    sender_mission_control = SenderToMissionControl()
    receiver_mission_control = ReceiverFromMissionControl()

    sender_rover = SenderToRover()
    receiver_rover = ReceiverFromRover()

    protocol_server = MyCommunicationProtocol(sender_mission_control, receiver_mission_control)
    protocol_client = MyCommunicationProtocol(sender_rover, receiver_rover)
        
    # Initialise le serveur sur server_address
    protocol_server.initialize_server(repeater_address)
    # Établir la connexion avec le Rover
    protocol_client.establish_connection(rover_address)
    
    # Initialisation du rover
    rover = Rover(position_x_start, position_y_start, orientation_start)

    try :
        # Le Repeater agit en tant que relais entre MissionControl et Rover
        while True:
            # Collecte des commands
            commands = receiver_mission_control.receive_command(protocol_server)
            if not commands:
                break  # Fin de la communication

            # Réexpédier les commands à Rover
            sender_rover.send_command(protocol_client, commands._Command__command_order)

            # Recevoir les données de Rover
            rover, coords = receiver_rover.receive_command(protocol_client, rover)

            # Réexpédier les données à MissionControl
            sender_mission_control.send_command(protocol_server, rover, coords)

    finally :
        # Ferme les sockets
        protocol_server.close_connection()
        protocol_client.close_connection()

if __name__ == "__main__":
    main()
