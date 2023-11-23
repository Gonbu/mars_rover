import unittest
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.MissionRover.command import Command
from Domain.Topologie.position import Position
from Domain.Exploration.obstacle import Obstacle


class TestRover(unittest.TestCase):
    def setUp(self):
        self.planet = Planet(5, 5, [])
        self.rover = Rover(0, 0, 'N')

    def testForward(self):
        self.rover = self.rover.move_forward(self.planet)
        self.assertEqual(self.rover._Rover__position
                         ._Position__x
                         ._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 1)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testForwardOutOfLimit(self):
        self.rover = Rover(0, 5, 'N')

        self.rover = self.rover.move_forward(self.planet)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testBackwardOutOfLimit(self):
        self.rover = self.rover.move_backward(self.planet)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 5)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testBackward(self):
        self.rover = Rover(0, 4, 'N')

        self.rover = self.rover.move_backward(self.planet)
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
        commands = Command(['F'], True)
        self.rover, _ = commands.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position
                         ._Position__x
                         ._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 1)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testBackwardWithInstruction(self):
        self.rover = Rover(0, 4, 'N')

        commands = Command(['B'], True)
        self.rover, _ = commands.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 3)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'N')

    def testInstructions(self):
        commands = Command(['L', 'L', 'F', 'R', 'F', 'F', 'L', 'B', 'L', 'F', 'R'], True)
        self.rover, _ = commands.exec_commands(self.planet, self.rover)
        self.assertEqual(self.rover._Rover__position._Position__x._Coordinate__value, 5)
        self.assertEqual(self.rover._Rover__position._Position__y._Coordinate__value, 0)
        self.assertEqual(self.rover._Rover__orientation._Orientation__orientation, 'S')


if __name__ == '__main__':
    unittest.main()
