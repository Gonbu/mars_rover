# Entité
class Instruction:
    def __init__(self, instructions = [], is_valid = False):
        self.__instruction_order = instructions
        self.__forward = 'F'
        self.__backward = 'B'
        self.__left = 'L'
        self.__right = 'R'
        self.again = True
        self.__is_valid = is_valid

    def add_instruction(self):
        self.__instruction_order = []
        commands_string = input('Enter commands: ').replace(" ", "")
        if "Q" in commands_string :
            self.again = False
            return
        commands = list(commands_string)
        self.__is_valid = all(element == self.__forward or element == self.__backward or element == self.__left or element == self.__right for element in commands)
        
        if self.__is_valid :
            for command in commands :
                self.__instruction_order.append(command)
        else:
            print('Invalid command list')
        pass

    def exec_commands(self, planet, rover):
        if self.__is_valid == False:
            return rover
        for command in self.__instruction_order:
            if command == 'F':
                rover, is_obstacle = rover.move_forward(planet)
                if is_obstacle :
                    break
            elif command == 'B':
                rover, is_obstacle = rover.move_backward(planet)
                if is_obstacle :
                    break
            elif command == 'L':
                rover = rover.turn_left()
            elif command == 'R':
                rover = rover.turn_right()

        return rover