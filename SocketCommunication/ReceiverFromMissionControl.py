from Domain.Communication.CommunicationAbstraction import CommandReceiver
from Domain.MissionRover.command import Command

# Classe qui reçoit les données envoyées par MissionControl
class ReceiverFromMissionControl(CommandReceiver):
    def receive_command(self, protocol):
        data = protocol.receive_data_with_length(protocol)

        # Décodage des données
        commands_received = data.decode('utf-8')
        commands = Command(commands_received, True)
        return commands