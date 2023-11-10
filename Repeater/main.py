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
from SocketCommunication.CommandReceiverRover import CommandReceiverRover
from SocketCommunication.CommandSenderRover import CommandSenderRover
from SocketCommunication.CommandReceiverMissionControl import CommandReceiverMissionControl
from SocketCommunication.CommandSenderMissionControl import CommandSenderMissionControl
from Missions.marsMission import *

<<<<<<< HEAD
def main() :
    # Définit l'adresse IP et le port du Rover auquel se connecter

    sender_mission_control = CommandSenderMissionControl()
    receiver_mission_control = CommandReceiverMissionControl()
=======
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
>>>>>>> 494897a (planet and rover comes from MissionControl With Repeater)

    sender_rover = CommandSenderRover()
    receiver_rover = CommandReceiverRover()

<<<<<<< HEAD
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
=======
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
>>>>>>> 494897a (planet and rover comes from MissionControl With Repeater)
