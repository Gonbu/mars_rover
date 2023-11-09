from Domain.Topologie.position import Position
from Domain.Topologie.orientation import Orientation

#Object-Value
class Rover:
    def __init__(self, x, y, orientation):
        self.__position = Position(x, y)
        self.__orientation = Orientation(orientation)

    def __repr__(self):
        return f"{self.__position._Position__x._Coordinate__value},{self.__position._Position__y._Coordinate__value},{self.__orientation._Orientation__orientation}"

    def move_forward(self, planet):
        position, obstacle = self.__orientation.update_position('F', self.__position, planet)
        new_rover = Rover(position._Position__x._Coordinate__value, position._Position__y._Coordinate__value, self.__orientation._Orientation__orientation)
        new_rover.to_string()
        return new_rover, obstacle
        
    def move_backward(self, planet):
        position, obstacle = self.__orientation.update_position('B', self.__position, planet)
        new_rover = Rover(position._Position__x._Coordinate__value, position._Position__y._Coordinate__value, self.__orientation._Orientation__orientation)
        new_rover.to_string()
        return new_rover, obstacle

    def turn_left(self):
        orientation = self.__orientation.update_orientation('L')
        new_rover = Rover(self.__position._Position__x._Coordinate__value, self.__position._Position__y._Coordinate__value, orientation._Orientation__orientation)
        new_rover.to_string()
        return new_rover
        
    def turn_right(self):
        orientation = self.__orientation.update_orientation('R')
        new_rover = Rover(self.__position._Position__x._Coordinate__value, self.__position._Position__y._Coordinate__value, orientation._Orientation__orientation)
        new_rover.to_string()
        return new_rover

    def to_string(self):
        print(
            f"Rover is at {self.__position._Position__x._Coordinate__value}, {self.__position._Position__y._Coordinate__value} facing {self.__orientation._Orientation__orientation}")

    def from_repr(self, rover_repr):
        #return f"{self.__position._Position__x._Coordinate__value},{self.__position._Position__y._Coordinate__value},{self.__orientation._Orientation__orientation}"
        try :
            self.__position._Position__x._Coordinate__value = int(rover_repr[0])
            self.__position._Position__y._Coordinate__value = int(rover_repr[1])
            self.__orientation._Orientation__orientation = rover_repr[2]
        except :
            pass