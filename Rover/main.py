import socket
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.rover import Rover
from Domain.MissionRover.command import Command
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
# from Domain.Communication.CommunicationAbstraction import CommandReceiver, CommandSender
from SocketCommunication.ReceiverFromMissionControl import ReceiverFromMissionControl
from SocketCommunication.SenderToMissionControl import SenderToMissionControl
from Missions.marsMission import *

def main():
    # Initialisation des objets de communication
    sender = SenderToMissionControl()
    receiver = ReceiverFromMissionControl()
    protocol = MyCommunicationProtocol(sender, receiver)

    # Initialiser le serveur dans le protocole
    protocol.initialize_server(rover_address)

    # Initialisation du rover
    rover = Rover(position_x_start, position_y_start, orientation_start)

    try:
        # Attendez les données du client et renvoyez-les
        while True:
            commands = receiver.receive_command(protocol)
            if not commands:
                break  # Fin de la communication

            rover, obstacle = commands.exec_commands(mars, rover)
            
            sender.send_command(protocol, rover, obstacle)
    finally:
        # Fermez les sockets
        protocol.close_connection()

if __name__ == "__main__":
    main()
