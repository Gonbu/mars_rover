import unittest
import Rover.main as r
import MissionControl.main as mc
from Domain.Exploration import planet
from Domain.MissionRover import rover, instruction


class TestServer:
    def __init__(self):
        self.server_address = ('127.0.0.1', 12345)

        self.sender = r.MyCommandSender()
        self.receiver = r.MyCommandReceiver()
        self.protocol = r.MyCommunicationProtocol(self.sender, self.receiver)


class TestClient:
    def __init__(self):
        self.server_address = ('127.0.0.1', 12345)

        self.sender = mc.MyCommandSender()
        self.receiver = mc.MyCommandReceiver()
        self.protocol = mc.MyCommunicationProtocol(self.sender, self.receiver)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.server = TestServer()
        self.client = TestClient()
        self.mars = planet.Planet(5, 5, None)
        self.curiosity = rover.Rover(0, 0, 'N')

    def testInitAndCloseProtocol(self):
        self.server.protocol.initialize_server(self.server.server_address)
        unittest.TestCase.assertEqual(self, self.server.protocol.client_socket, None)




    def testSendAndReceive(self):
        pass


if __name__ == '__main__':
    unittest.main()
