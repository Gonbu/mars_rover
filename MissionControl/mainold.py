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
    def send_command(self, instructions):
        serialized_instructions = pickle.dumps(instructions)
        protocol.client_socket.send(serialized_instructions)

class MyCommandReceiver(CommandReceiver):
    def receive_command(self):
        data = protocol.client_socket.recv(1024)
        command_obj = pickle.loads(data)
        return command_obj

# Définit l'adresse IP et le port du serveur auquel se connecter
server_address = ('127.0.0.1', 12345)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol = MyCommunicationProtocol(sender, receiver)

protocol.establish_connection(server_address)

while True:
    instructions = instruction.Instruction()
    instructions.add_instruction()
    sender.send_command(instructions)
    #data = receiver.receive_command()
    #print("Serveur dit : {}".format(data))

# Ferme le socket client
client_socket.close()
