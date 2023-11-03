import socket
import pickle
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)   
from Domain.MissionRover import rover
from Domain.Exploration import planet
from Domain.MissionRover import instruction
from Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from Communication.ProtocolCommunication import MyCommunicationProtocol

class MyCommandSender(CommandSender):
    def send_command(self, curiosity):
        data_to_send = (curiosity)
        serialized_data = pickle.dumps(data_to_send)
        # Vous pouvez également envoyer la longueur des données en tant que préfixe
        data_length = len(serialized_data).to_bytes(4, byteorder='big')  # 4 bytes for data length
        data_to_send = data_length + serialized_data

        # Maintenant, vous envoyez les données avec la longueur en tant que préfixe
        protocol.client_socket.sendall(data_to_send)

class MyCommandReceiver(CommandReceiver):
    def receive_command(self):
        # Attendez de recevoir la longueur des données (4 octets)
        data_length_bytes = protocol.client_socket.recv(4)
        data_length = int.from_bytes(data_length_bytes, byteorder='big')
        # Maintenant, attendez de recevoir les données réelles en utilisant la longueur
        data = b""
        while len(data) < data_length:
            chunk = protocol.client_socket.recv(data_length - len(data))
            if not chunk:
                raise Exception("Connexion interrompue avant la fin de la réception des données.")
            data += chunk
        (instructions, mars, curiosity) = pickle.loads(data)
        return instructions, mars, curiosity


server_address = ('127.0.0.1', 12345)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol = MyCommunicationProtocol(sender, receiver)

# Initialiser le serveur dans le protocole
protocol.initialize_server(server_address)
""" mars = planet.Planet(5, 5, None)
curiosity = rover.Rover(0, 0, 'N') """

# Attendez les données du client et renvoyez-les
while True:
    instructions, mars, curiosity = receiver.receive_command()
    if not instructions:
        break  # Fin de la communication
    print(instructions._Instruction__instruction_order)
    
    curiosity = instructions.exec_commands(mars, curiosity)

    sender.send_command(curiosity)

# Fermez les sockets
protocol.close_connection()