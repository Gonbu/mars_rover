import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.command import Command

class MissionControlRunner:
    def __init__(self, sender, receiver, protocol, rover, server_address):
        self.sender = sender
        self.receiver = receiver
        self.protocol = protocol
        self.rover = rover
        self.server_address = server_address

    def run(self):
        try:
            while True:
                commands = Command()
                commands.add_command()

                self.sender.send_command(self.protocol, commands._Command__command_order)
                self.rover, obstacle = self.receiver.receive_command(self.protocol, self.rover)

                self.rover.to_string()
                if len(obstacle) > 0:
                    print("Obstacle : {}".format(obstacle))
        finally:
            self.protocol.client_socket.close()
