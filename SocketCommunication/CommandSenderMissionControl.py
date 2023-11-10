from Domain.Communication.CommunicationAbstraction import CommandSender

# Classe qui envoie des données à MissionControl
class CommandSenderMissionControl(CommandSender):
    def send_command(self, protocol, rover, obstacle):
        if not obstacle :
            obstacle = []
        data_to_send = protocol.encode(rover, *obstacle)
        protocol.client_socket.sendall(data_to_send)