import socket
import pickle
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.rover import Rover
from Domain.MissionRover.instruction import Instruction
from Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from Communication.ProtocolCommunication import MyCommunicationProtocol

class MyCommandSenderMissionControl(CommandSender):
    def send_command(self, protocol, rover, coords):
        data_to_send = protocol.encode(rover, *coords)
        protocol.client_socket.sendall(data_to_send)

class MyCommandSenderRover(CommandSender):
    def send_command(self, protocol, instructions):
        data_to_send = protocol.encode(instructions)
        protocol.client_socket.sendall(data_to_send)

class MyCommandReceiverMissionControl(CommandReceiver):
    def receive_command(self, protocol):
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
        instructions_received = data.decode('utf-8')
        instructions = Instruction(instructions_received, True)
        return instructions
    
class MyCommandReceiverRover(CommandReceiver):
    def receive_command(self, protocol):
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
        rover = Rover(0, 0, 'N')
        rover.from_repr(rover_str)
        return rover, coords

def main() :
    # Définit l'adresse IP et le port du Rover auquel se connecter
    rover_address = ('127.0.0.1', 12345)
    server_address = ('127.0.0.1', 12346)

    sender_mission_control = MyCommandSenderMissionControl()
    receiver_mission_control = MyCommandReceiverMissionControl()

    sender_rover = MyCommandSenderRover()
    receiver_rover = MyCommandReceiverRover()

    protocol_server = MyCommunicationProtocol(sender_mission_control, receiver_mission_control)
    protocol_client = MyCommunicationProtocol(sender_rover, receiver_rover)
        
    # Initialise le serveur sur server_address
    protocol_server.initialize_server(server_address)
    # Établir la connexion avec le Rover
    protocol_client.establish_connection(rover_address)

    try :
        # Le Repeater agit en tant que relais entre MissionControl et Rover
        while True:
            # Collecte des instructions
            instructions = receiver_mission_control.receive_command(protocol_server)
            if not instructions:
                break  # Fin de la communication

            # Réexpédier les instructions à Rover
            sender_rover.send_command(protocol_client, instructions._Instruction__instruction_order)

            # Recevoir les données de Rover
            rover, coords = receiver_rover.receive_command(protocol_client)

            # Réexpédier les données à MissionControl
            sender_mission_control.send_command(protocol_server, rover, coords)

    finally :
        # Ferme les sockets
        protocol_server.close_connection()
        protocol_client.close_connection()

if __name__ == "__main__":
    main()
