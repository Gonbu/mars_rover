# Envoie des données à Rover
from Domain.Communication.CommunicationAbstraction import CommandSender

class CommandSenderRover(CommandSender):
    def send_command(self, protocol, instructions):
        data_to_send = protocol.encode(instructions)
        protocol.client_socket.sendall(data_to_send)