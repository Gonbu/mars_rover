import unittest
import MissionControl
import Domain


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.server_address = ('127.0.0.1', 12345)
        self.sender = MissionControl.main.MyCommandSender()
        self.receiver = MissionControl.main.MyCommandReceiver()
        self.protocol = MissionControl.main.MyCommunicationProtocol(self.sender, self.receiver)
        self.mars = Domain.Exploration.planet.Planet(5, 5, None)
        self.curiosity = Domain.MissionRover.rover.Rover(0, 0, 'N')

    def testInitAndCloseProtocol(self):
        self.protocol.initialize_server(self.server_address)
        unittest.TestCase.assertEqual(self, self.protocol.client_address, self.server_address)

        self.protocol.close_connection()
        unittest.TestCase.assertEqual(self, self.protocol.client_socket, None)

    def testSendAndReceive(self):
        self.protocol.initialize_server(self.server_address)
        instructions = Domain.MissionRover.instruction.Instruction()

        instructions.add_instruction()
        self.sender.send_command(instructions)

        data = self.receiver.receive_command()
        unittest.TestCase.assertEqual(self, data, instructions)
        self.protocol.close_connection()


if __name__ == '__main__':
    unittest.main()
