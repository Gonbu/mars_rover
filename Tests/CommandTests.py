from unittest import TestCase, mock, main
import time
import threading
import Rover.main as r
import MissionControl.main as mc
from Domain.Topologie import position
from Domain.Exploration import planet, obstacle
from Domain.MissionRover import rover, command


class TestServer:
    def __init__(self):
        self.sender = r.SenderToMissionControl()
        self.receiver = r.ReceiverFromMissionControl()
        self.protocol = r.MyCommunicationProtocol(self.sender, self.receiver)


class TestClient:
    def __init__(self):
        self.sender = mc.SenderToRover()
        self.receiver = mc.ReceiverFromRover()
        self.protocol = mc.MyCommunicationProtocol(self.sender, self.receiver)


class CommandTests(TestCase):
    def setUp(self):
        self.server_address = ('127.0.0.1', 12345)
        self.server = TestServer()
        self.client = TestClient()
        self.mars = planet.Planet(5, 5, None)
        self.curiosity = rover.Rover(0, 0, 'N')

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self.server.protocol.initialize_server,
                                              args=(self.server_address,))
        self.server_thread.start()

        # Allow some time for the server to start before connecting the client
        time.sleep(1)

        # Connect the client to the server
        self.client.protocol.establish_connection(self.server_address)

    def testAddCommandsValidInput(self):
        commands = command.Command()

        # Use mock to simulate user input
        with mock.patch('builtins.input', return_value='FFLBR'):
            commands.add_command()

            self.assertEqual(commands._Command__command_order, ['F', 'F', 'L', 'B', 'R'])
            self.assertEqual(commands._Command__is_valid, True)

    def testAddCommandsInvalidInput(self):
        commands = command.Command()

        # Use mock to simulate user input
        with mock.patch('builtins.input', return_value='invalid_input'):
            commands.add_command()

            self.assertEqual(commands._Command__command_order, [])
            self.assertEqual(commands._Command__is_valid, False)

    def testExecCommandsValid(self):
        commands = command.Command(['F', 'F', 'L', 'B', 'R'], True)

        self.curiosity, obstacles = commands.exec_commands(self.mars, self.curiosity)

        self.assertEqual(self.curiosity._Rover__position._Position__x._Coordinate__value, 1)
        self.assertEqual(self.curiosity._Rover__position._Position__y._Coordinate__value, 2)
        self.assertEqual(self.curiosity._Rover__orientation._Orientation__orientation, 'N')
        self.assertIsNone(obstacles)

    def testExecCommandsInvalid(self):
        commands = command.Command(['invalid_input'], False)

        self.curiosity, obstacles = commands.exec_commands(self.mars, self.curiosity)

        self.assertEqual(self.curiosity._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.curiosity._Rover__position._Position__y._Coordinate__value, 0)
        self.assertEqual(self.curiosity._Rover__orientation._Orientation__orientation, 'N')
        self.assertIsNone(obstacles)

    def testExecCommandsObstacle(self):
        self.mars = planet.Planet(5, 5, [obstacle.Obstacle(None, position.Position(0, 5))])
        commands = command.Command(['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], True)

        self.curiosity, obstacles = commands.exec_commands(self.mars, self.curiosity)

        self.assertEqual(self.curiosity._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.curiosity._Rover__position._Position__y._Coordinate__value, 4)
        self.assertEqual(self.curiosity._Rover__orientation._Orientation__orientation, 'N')
        self.assertEqual(obstacles, [0, 5])

    def testSendAndReceive(self):
        # Send a command from the client to the server and receive the response
        response = self.client.protocol.send_and_receive(self.client.protocol.client_socket, "test")

        # Check if the response is the same as the one sent
        self.assertEqual(response, "test")

    def tearDown(self):
        # Close the client connection
        self.client.protocol.close_connection()

        # Wait for the server thread to finish
        self.server_thread.join()


if __name__ == '__main__':
    main()
