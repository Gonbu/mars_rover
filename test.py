import pickle
import subprocess
import time
import unittest
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.MissionRover.instruction import Instruction
from Domain.Topologie.position import Position
from Domain.Exploration.obstacle import Obstacle
from Communication.ProtocolCommunication import MyCommunicationProtocol



class TestRover(unittest.TestCase):
    # def setUp(self):
    #     self.planet = Planet(5, 5, [])
    #     self.rover = Rover(0, 0, 'N')

    # def testForward(self):
    #     self.rover, _ = self.rover.move_forward(self.planet)
    #     self.assertEqual(self.rover._Rover__position
    #                      ._Position__x
    #                      ._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 1)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    # def testForwardOutOfLimit(self):
    #     self.rover = Rover(0, 5, 'N')

    #     self.rover, _ = self.rover.move_forward(self.planet)
    #     self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    # def testBackwardOutOfLimit(self):
    #     self.rover, _ = self.rover.move_backward(self.planet)
    #     self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 5)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    # def testBackward(self):
    #     self.rover = Rover(0, 4, 'N')

    #     self.rover, _ = self.rover.move_backward(self.planet)
    #     self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 3)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    # def testTurnRight(self):
    #     self.rover = self.rover.turn_right()
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'E')

    # def testTurnLeft(self):
    #     self.rover = self.rover.turn_left()
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'W')

    # def testForwardWithInstruction(self):
    #     self.instructions = Instruction(['F'], True)
    #     self.rover = self.instructions.exec_commands(self.planet, self.rover)
    #     self.assertEqual(self.rover._Rover__position
    #                      ._Position__x
    #                      ._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 1)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    # def testBackwardWithInstruction(self):
    #     self.rover = Rover(0, 4, 'N')

    #     self.instructions = Instruction(['B'], True)
    #     self.rover = self.instructions.exec_commands(self.planet, self.rover)
    #     self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 3)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    # def testInstructions(self):
    #     self.instructions = Instruction(['L', 'L', 'F', 'R', 'F', 'F', 'L', 'B', 'L', 'F', 'R'], True)
    #     self.rover = self.rover = self.instructions.exec_commands(self.planet, self.rover)
    #     self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 5)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'S')

    # def testObstacle(self):
    #     self.planet = Planet(5, 5, [Obstacle(None, Position(5, 5))])
    #     self.instructions = Instruction(['L', 'L', 'F', 'R', 'F', 'F', 'L', 'B', 'L', 'F', 'R'], True)
    #     self.rover = self.instructions.exec_commands(self.planet, self.rover)
    #     self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
    #     self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 5)
    #     self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'W')
            
    def testServerClientCommunication(self):
        server = 'Rover/main.py'
        client = 'MissionControl/main.py'
        server_process = subprocess.Popen(['python', server])
        time.sleep(1)
        # client_process = subprocess.Popen(['python', client], stdin=subprocess.PIPE, text=True)
        # time.sleep(1)
        with subprocess.Popen(['python', client], stdin=subprocess.PIPE,  stdout=subprocess.PIPE, text=True) as client_process:
            # Write to the client's stdin
            client_process.stdin.write("N\n")
            client_process.stdin.flush()
            client_process.stdin.write("FFF\n")
            client_process.stdin.flush()
            client_process.stdin.write("FRBF\n")
            client_process.stdin.flush()

            # Read the output of the client process
            # client_output, _ = client_process.communicate()

            # # Print the output
            # print("Client output:", client_output)


            # Wait for the client process to finish
            client_process.wait()
            # Wait for the server process to finish
            server_process.wait()

        
        print("All was successful")
        client_process.terminate()
        server_process.terminate()

    
        



if __name__ == '__main__':
    unittest.main()
