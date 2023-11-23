import copy
from Domain.Topologie.position import Position
from Domain.Topologie.orientation import Orientation

class Rover:
    def __init__(self, x, y, orientation):
        self.__position = Position(x, y)
        self.__orientation = Orientation(orientation)

    def __str__(self):
        return f"{self.__position},{self.__orientation}"

    def move_forward(self, planet):
        initial_position = copy.deepcopy(self.__position)
        position = self.__orientation.update_position('F', initial_position, planet)
        if position == self.__position :
            return self
        else :
            self.__position = position
        new_rover = copy.deepcopy(self)
        self.display_state()
        return new_rover
        
    def move_backward(self, planet):
        initial_position = copy.deepcopy(self.__position)
        position = self.__orientation.update_position('B', initial_position, planet)
        if position == self.__position :
            return self
        else :
            self.__position = position
        new_rover = copy.deepcopy(self)
        new_rover.display_state()
        return new_rover

    def turn_left(self):
        self.__orientation = self.__orientation.update_orientation('L')
        new_rover = copy.deepcopy(self)
        new_rover.display_state()
        return new_rover
        
    def turn_right(self):
        self.__orientation = self.__orientation.update_orientation('R')
        new_rover = copy.deepcopy(self)
        new_rover.display_state()
        return new_rover

    def display_state(self):
        print(
            f"Rover is at {self.__position} facing {self.__orientation}")

    def from_repr(self, rover_repr):
        self.__position = Position(int(rover_repr[0]), rover_repr[1])
        self.__orientation = Orientation(rover_repr[2])