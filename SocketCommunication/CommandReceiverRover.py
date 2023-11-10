from Domain.Communication.CommunicationAbstraction import CommandReceiver

# Classe qui reçoit les données envoyées par Rover
class CommandReceiverRover(CommandReceiver):
    def receive_command(self, protocol, rover):
        data = protocol.receive_data_with_length(protocol)

        # Décodage des données
        decoded_data = data.decode('utf-8')
        rover_str, coords = decoded_data.split(',')[0:3], list(map(int, decoded_data.split(',')[3:]))
        rover.from_repr(rover_str)
        return rover, coords