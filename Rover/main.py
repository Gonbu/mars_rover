from dis import Instruction
import socket
import pickle
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)   
from Domain.MissionRover.rover import Rover
from Domain.MissionRover.instruction import Instruction
from Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from Communication.ProtocolCommunication import MyCommunicationProtocol
from Domain.MissionRover.missionInitializer import *

class MyCommandSender(CommandSender):
    def send_command(self, rover, coords):
        data_to_send = protocol.encode(rover, *coords)
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
        instructions_received = data.decode('utf-8')
        instructions = Instruction(instructions_received, True)
        return instructions


server_address = ('127.0.0.1', 12345)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol = MyCommunicationProtocol(sender, receiver)

# Initialiser le serveur dans le protocole
protocol.initialize_server(server_address)

# Initialisation du rover
rover = Rover(position_x_start, position_y_start, orientation_start)

# Attendez les données du client et renvoyez-les
while True:
    instructions = receiver.receive_command()
    if not instructions:
        break  # Fin de la communication
    
    rover, obstacle = instructions.exec_commands(mars, rover)

    if obstacle["is_obstacle"] :
        sender.send_command(rover, [obstacle["position"]["x"], obstacle["position"]["y"]])
    else :
        sender.send_command(rover, [])

# Fermez les sockets
protocol.close_connection()