from Domain.Communication.CommunicationAbstraction import CommandSender

# Classe qui envoie des données à MissionControl
class CommandSenderMissionControl(CommandSender):
    def send_command(self, protocol, rover, coords):
        data_to_send = protocol.encode(rover, *coords)
        protocol.client_socket.sendall(data_to_send)