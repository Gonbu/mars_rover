# Entité
import copy


class Command:
    def __init__(self, commands = [], is_valid = False):
        self.__command_order = commands
        self.__forward = 'F'
        self.__backward = 'B'
        self.__left = 'L'
        self.__right = 'R'
        self.again = True
        self.__is_valid = is_valid

    def add_command(self):
        self.__command_order = []
        commands_string = input('Enter commands: ').replace(" ", "")
        if "Q" in commands_string :
            self.again = False
            return
        commands = list(commands_string)
        self.__is_valid = all(element == self.__forward or element == self.__backward or element == self.__left or element == self.__right for element in commands)
        
        if self.__is_valid :
            for command in commands :
                self.__command_order.append(command)
        else:
            print('Invalid command list')
        pass

    def exec_commands(self, planet, rover):
        if self.__is_valid == False:
            return rover, None
        for command in self.__command_order:
            actual_rover = rover
            if command == 'F':
                rover = rover.move_forward(planet)
                if actual_rover == rover :
                    actual_position = copy.deepcopy(actual_rover._Rover__position)
                    direction_x, direction_y = rover._Rover__orientation.get_direction_x_y('F')
                    obstacle_position = rover._Rover__orientation.position_after_movement(planet, actual_position, direction_x, direction_y)

                    print("rover position x", rover._Rover__position._Position__x._Coordinate__value)
                    print("rover position y", rover._Rover__position._Position__y._Coordinate__value)
                    return rover, [obstacle_position._Position__x._Coordinate__value, obstacle_position._Position__y._Coordinate__value]
            elif command == 'B':
                rover = rover.move_backward(planet)
                if actual_rover == rover :
                    direction_x, direction_y = rover._Rover__orientation.get_direction_x_y('B')
                    obstacle_position = rover._Rover__orientation.position_after_movement(planet, rover._Rover__position, direction_x, direction_y)
                    return rover, [obstacle_position._Position__x._Coordinate__value, obstacle_position._Position__y._Coordinate__value]
            elif command == 'L':
                rover = rover.turn_left()
            elif command == 'R':
                rover = rover.turn_right()

        return rover, None