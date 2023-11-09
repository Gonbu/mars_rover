import unittest
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.MissionRover.instruction import Instruction
from Domain.Topologie.position import Position
from Domain.Exploration.obstacle import Obstacle


class TestRover(unittest.TestCase):
    def setUp(self):
        self.planet = Planet(5, 5, [])
        self.rover = Rover(0, 0, 'N')

    def testForward(self):
        self.rover, _ = self.rover.move_forward(self.planet)
        self.assertEqual(self.rover._Rover__position
                         ._Position__x
                         ._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 1)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testForwardOutOfLimit(self):
        self.rover = Rover(0, 5, 'N')

        self.rover, _ = self.rover.move_forward(self.planet)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testBackwardOutOfLimit(self):
        self.rover, _ = self.rover.move_backward(self.planet)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 5)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testBackward(self):
        self.rover = Rover(0, 4, 'N')

        self.rover, _ = self.rover.move_backward(self.planet)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 3)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testTurnRight(self):
        self.rover = self.rover.turn_right()
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'E')

    def testTurnLeft(self):
        self.rover = self.rover.turn_left()
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'W')

    def testForwardWithInstruction(self):
        self.instructions = Instruction(['F'], True)
        self.rover = self.instructions.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position
                         ._Position__x
                         ._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 1)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testBackwardWithInstruction(self):
        self.rover = Rover(0, 4, 'N')

        self.instructions = Instruction(['B'], True)
        self.rover = self.instructions.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 3)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testInstructions(self):
        self.instructions = Instruction(['L', 'L', 'F', 'R', 'F', 'F', 'L', 'B', 'L', 'F', 'R'], True)
        self.rover = self.rover = self.instructions.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 5)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'S')

    def testObstacle(self):
        self.planet = Planet(5, 5, [Obstacle(None, Position(5, 5))])
        self.instructions = Instruction(['L', 'L', 'F', 'R', 'F', 'F', 'L', 'B', 'L', 'F', 'R'], True)
        self.rover = self.instructions.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 5)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'W')


if __name__ == '__main__':
    unittest.main()
