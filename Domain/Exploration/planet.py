import copy
from Domain.Exploration.obstacle import Obstacle
from Domain.Exploration.planetInterface import PlanetInterface
from Domain.Topologie.position import Position

class Planet(PlanetInterface):
    def __init__(self, size_x, size_y, obstacles=None):
        self.__size_x = size_x
        self.__size_y = size_y
        if obstacles is None:
            obstacles = [Obstacle(self) for _ in range(size_x * size_y // 10)]
        self.__obstacles = obstacles

    def check_limit_planet(self, position):
        new_x_position, new_y_position = position.modulo(self.__size_x, self.__size_y)
        return Position(new_x_position, new_y_position)

    def is_obstacle_at_position(self, position) :
        position = self.check_limit_planet(position)
        for obstacle in self.__obstacles :
            if obstacle.compare_obstacle_and_position(position) :
                return True
        return False