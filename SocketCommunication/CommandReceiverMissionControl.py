from Domain.Communication.CommunicationAbstraction import CommandReceiver
from Domain.MissionRover.instruction import Instruction

class CommandReceiverMissionControl(CommandReceiver):
    def receive_command(self, protocol):
        data = protocol.receive_data_with_length(protocol)

        # Décodage des données
        instructions_received = data.decode('utf-8')
        instructions = Instruction(instructions_received, True)
        return instructions