class RoverOverNetwork:
    def __init__(self, rover, protocol, sender, receiver, planet):
        self.rover = rover
        self.protocol = protocol
        self.sender = sender
        self.receiver = receiver
        self.planet = planet

    def run(self):
        try:
            while True:
                commands = self.receiver.receive_command(self.protocol)
                if not commands:
                    break

                self.rover, obstacle = commands.exec_commands(self.planet, self.rover)

                self.sender.send_command(self.protocol, self.rover, obstacle)
        finally:
            self.protocol.close_connection()
