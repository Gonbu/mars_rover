from Domain.Topologie.position import Position

#O-V
class Orientation:
    def __init__(self, orientation):
        self.__orientation = orientation
        self.__movements = {
            'N': (0, 1),
            'E': (1, 0),
            'S': (0, -1),
            'W': (-1, 0)
        }
        self.__opposites = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}
        self.__rotations = {
            'N': {'L': 'W', 'R': 'E'},
            'E': {'L': 'N', 'R': 'S'},
            'S': {'L': 'E', 'R': 'W'},
            'W': {'L': 'S', 'R': 'N'}
        }

    def __str__(self) :
        return f"{self.__orientation}"

    def update_position(self, direction, position, planet):
        direction_x, direction_y = self.get_direction_x_y(direction)
    
        if not planet.is_obstacle_at_position(Position(direction_x+position._Position__x._Coordinate__value, direction_y+position._Position__y._Coordinate__value)) :
            position = self.position_after_movement(planet, position, direction_x, direction_y)
        else :
            print("Obstacle rencontré")
        return Position(position._Position__x._Coordinate__value, position._Position__y._Coordinate__value)

    def get_direction_x_y(self, direction) :
        if direction == 'F':
            direction_x, direction_y = self.__movements[self.__orientation]
            return direction_x, direction_y
        elif direction == 'B':
            direction_x, direction_y = self.__movements[self.__opposites[self.__orientation]]
            return direction_x, direction_y
        else:
            raise ValueError("Invalid direction")

    def position_after_movement(self, planet, position, direction_x, direction_y) :
        position._Position__x._Coordinate__value += direction_x
        position._Position__y._Coordinate__value += direction_y
        position = planet.check_limit_planet(position)
        return position

    def update_orientation(self, rotation):
        rotations = self.__rotations

        if rotation in ['L', 'R']:
            return Orientation(rotations[self.__orientation][rotation])
        else:
            raise ValueError("Invalid rotation")

