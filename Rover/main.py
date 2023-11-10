import socket
import sys
import os
from dis import Instruction
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.rover import Rover
from Domain.MissionRover.instruction import Instruction
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
# from Domain.Communication.CommunicationAbstraction import CommandReceiver, CommandSender
from SocketCommunication.CommandReceiverMissionControl import CommandReceiverMissionControl
from SocketCommunication.CommandSenderMissionControl import CommandSenderMissionControl
from Missions.marsMission import *

def main():
    # Initialisation des objets de communication
    sender = CommandSenderMissionControl()
    receiver = CommandReceiverMissionControl()
    protocol = MyCommunicationProtocol(sender, receiver)

    # Définition de l'adresse IP et du port du serveur auquel se connecter
    server_address = ('127.0.0.1', 12345)

    # Initialiser le serveur dans le protocole
    protocol.initialize_server(server_address)

    # Initialisation du rover
    rover = Rover(position_x_start, position_y_start, orientation_start)

    try:
        # Attendez les données du client et renvoyez-les
        while True:
            instructions = receiver.receive_command(protocol)
            if not instructions:
                break  # Fin de la communication

            rover, obstacle = instructions.exec_commands(mars, rover)

            if obstacle["is_obstacle"]:
                sender.send_command(protocol, rover, [obstacle["position"]["x"], obstacle["position"]["y"]])
            else:
                sender.send_command(protocol, rover, [])
    finally:
        # Fermez les sockets
        protocol.close_connection()

if __name__ == "__main__":
    main()
