import socket
import pickle
from Communication.CommunicationAbstraction import CommandSender, CommandReceiver

class MyCommunicationProtocol:
    def __init__(self, sender: CommandSender, receiver: CommandReceiver):
        self.sender = sender
        self.receiver = receiver
        self.client_socket = None
        self.client_address = None

    def initialize_server(self, server_address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)
        print("Le serveur écoute sur {}:{}.".format(*server_address))
        self.client_socket, self.client_address = self.server_socket.accept()

    def establish_connection(self, server_address):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(server_address)

    def send_and_receive(self, command):
        self.sender.send_command(self.client_socket, command)
        response = self.receiver.receive_command(self.client_socket)
        return response

    def close_connection(self):
        self.client_socket.close()

