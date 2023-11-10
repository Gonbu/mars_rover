# Entité
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
        obstacle = {"is_obstacle": False}
        if self.__is_valid == False:
            return rover, obstacle
        for command in self.__command_order:
            if command == 'F':
                rover, obstacle = rover.move_forward(planet)
                if obstacle["is_obstacle"] :
                    break
            elif command == 'B':
                rover, obstacle = rover.move_backward(planet)
                if obstacle["is_obstacle"] :
                    break
            elif command == 'L':
                rover = rover.turn_left()
            elif command == 'R':
                rover = rover.turn_right()

        return rover, obstacle