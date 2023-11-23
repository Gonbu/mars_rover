# import sys
# sys.path.append('../Rover')

import unittest
import time
import threading
import Rover.main as r
import MissionControl.main as mc
from Domain.Exploration import planet
from Domain.MissionRover import rover, instruction


class TestServer:
    def __init__(self):
        self.sender = r.MyCommandSender()
        self.receiver = r.MyCommandReceiver()
        self.protocol = r.MyCommunicationProtocol(self.sender, self.receiver)


class TestClient:
    def __init__(self):
        self.sender = mc.MyCommandSender()
        self.receiver = mc.MyCommandReceiver()
        self.protocol = mc.MyCommunicationProtocol(self.sender, self.receiver)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.server_address = ('127.0.0.1', 12345)
        self.server = TestServer()
        self.client = TestClient()
        self.mars = planet.Planet(5, 5, None)
        self.curiosity = rover.Rover(0, 0, 'N')

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self.server.protocol.initialize_server, args=(self.server_address,))
        self.server_thread.start()

        # Allow some time for the server to start before connecting the client
        time.sleep(1)

        # Connect the client to the server
        self.client.protocol.establish_connection(self.server_address)

    def testSendCommand(self):
        # Send a command from the client to the server
        self.client.protocol.send_command(self.client.protocol.client_socket, "test")

        # Receive the command on the server side
        command = self.server.protocol.receive_command(self.server.protocol.client_socket)

        # Check if the command is the same as the one sent
        self.assertEqual(command, "test")

    def tearDown(self):
        # Close the client connection
        self.client.protocol.close_connection()

        # Wait for the server thread to finish
        self.server_thread.join()


if __name__ == '__main__':
    unittest.main()
