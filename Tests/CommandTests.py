import unittest
from MissionControl.main import MyCommandSender, MyCommandReceiver, MyCommunicationProtocol
from Domain.Exploration import planet
from Domain.MissionRover import rover, instruction


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.server_address = ('127.0.0.1', 12345)
        self.sender = MyCommandSender()
        self.receiver = MyCommandReceiver()
        self.protocol = MyCommunicationProtocol(self.sender, self.receiver)
        self.mars = planet.Planet(5, 5, None)
        self.curiosity = rover.Rover(0, 0, 'N')

    def testInitAndCloseProtocol(self):
        self.protocol.initialize_server(self.server_address)
        unittest.TestCase.assertEqual(self, self.protocol.client_address, self.server_address)

        self.protocol.close_connection()
        unittest.TestCase.assertEqual(self, self.protocol.client_socket, None)

    def testSendAndReceive(self):
        self.protocol.initialize_server(self.server_address)
        instructions = instruction.Instruction()
        instructions.add_instruction()

        self.sender.send_command(instructions)
        data = self.receiver.receive_command()
        unittest.TestCase.assertEqual(self, data, instructions)
        self.protocol.close_connection()


if __name__ == '__main__':
    unittest.main()
