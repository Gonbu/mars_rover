from Domain.Communication.CommunicationAbstraction import CommandReceiver
from Domain.MissionRover.command import Command

class ReceiverFromMissionControl(CommandReceiver):
    def receive_command(self, protocol):
        data = protocol.receive_data_with_length(protocol)

