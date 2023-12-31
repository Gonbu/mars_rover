class RepeaterRunner:
    def __init__(self, sender_mission_control, receiver_mission_control, sender_rover, receiver_rover, protocol_server, protocol_client, rover):
        self.sender_mission_control = sender_mission_control
        self.receiver_mission_control = receiver_mission_control
        self.sender_rover = sender_rover
        self.receiver_rover = receiver_rover
        self.protocol_server = protocol_server
        self.protocol_client = protocol_client
        self.rover = rover

    def run(self):
        try:
            while True:
                commands = self.receiver_mission_control.receive_command(self.protocol_server)
                if not commands:
                    break
                self.sender_rover.send_command(self.protocol_client, commands._Command__command_order)
                self.rover, coords = self.receiver_rover.receive_command(self.protocol_client, self.rover)
                self.sender_mission_control.send_command(self.protocol_server, self.rover, coords)

        finally:
            self.protocol_server.close_connection()
            self.protocol_client.close_connection()
