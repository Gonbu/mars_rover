from Domain.Communication.CommunicationAbstraction import CommandSender

# Classe qui envoie des données à Rover
class SenderToRover(CommandSender):
    def send_command(self, protocol, commands):
        data_to_send = protocol.encode(commands)
        protocol.client_socket.sendall(data_to_send)