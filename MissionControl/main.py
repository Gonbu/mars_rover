import socket
import pickle
import threading
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
    def send_command(self, instructions, mars, curiosity):
        data_to_send = (instructions, mars, curiosity)
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
        (curiosity) = pickle.loads(data)
        return curiosity

# Définit l'adresse IP et le port du serveur auquel se connecter
server_address = ('127.0.0.1', 12345)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol = MyCommunicationProtocol(sender, receiver)

protocol.establish_connection(server_address)

mars = planet.Planet(5, 5, None)
curiosity = rover.Rover(0, 0, 'N')

while True:
    instructions = instruction.Instruction()
    instructions.add_instruction()
    sender.send_command(instructions, mars, curiosity)
    # Recevez l'état mis à jour de Rover
    curiosity = receiver.receive_command()

    # Traitez les données reçues de Rover
    print("Rover renvoie : {}".format(curiosity))

# Ferme le socket client
client_socket.close()
