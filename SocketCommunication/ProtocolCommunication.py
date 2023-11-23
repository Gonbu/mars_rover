import socket
import pickle
from Domain.Communication.CommunicationAbstraction import CommandSender, CommandReceiver

class MyCommunicationProtocol(CommandSender, CommandReceiver) :
    def __init__(self, sender, receiver):
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

    def send_command(self, socket, command):
        pass

    def receive_command(self, socket):
        pass
    
    def encode(self, *values):
        data_to_send = ",".join(map(str, values))
        data_length = len(data_to_send).to_bytes(4, byteorder='big')
        data_to_send = data_length + data_to_send.encode('utf-8')
        return data_to_send
    
    def receive_data_with_length(self, protocol) :
        data_length_bytes = protocol.client_socket.recv(4)
        data_length = int.from_bytes(data_length_bytes, byteorder='big')

        data = b""
        while len(data) < data_length:
            chunk = protocol.client_socket.recv(data_length - len(data))
            if not chunk:
                raise Exception("Connexion interrompue avant la fin de la réception des données.")
            data += chunk

        return data

    def close_connection(self):
        self.client_socket.close()

