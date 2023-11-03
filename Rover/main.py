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
    def send_command(self, command):
        serialized_obj = pickle.dumps(command)
        protocol.client_socket.send(serialized_obj)

class MyCommandReceiver(CommandReceiver):
    def receive_command(self):
        data = protocol.client_socket.recv(1024)
        command_obj = pickle.loads(data)
        return command_obj

server_address = ('127.0.0.1', 12345)

sender = MyCommandSender()
receiver = MyCommandReceiver()
protocol = MyCommunicationProtocol(sender, receiver)

# Initialiser le serveur dans le protocole
protocol.initialize_server(server_address)
mars = planet.Planet(5, 5, None)
curiosity = rover.Rover(0, 0, 'N')

# Attendez les données du client et renvoyez-les
while True:
    instructions = receiver.receive_command()
    if not instructions:
        break  # Fin de la communication
    print("MissionControl dit : {}".format(instructions))
    print(instructions._Instruction__instruction_order)
    
    curiosity = instructions.exec_commands(mars, curiosity)
    print(curiosity)
    #response = Instruction("LLFF")
    #sender.send_command(response)

# Fermez les sockets
protocol.close_connection()