from Domain.Exploration.obstacle import Obstacle
from Domain.Exploration.planetInterface import PlanetInterface

#Objet-valeur
class Planet(PlanetInterface):
    def __init__(self, size_x, size_y, obstacles=None):
        self.__size_x = size_x
        self.__size_y = size_y
        if obstacles is None:
            obstacles = [Obstacle(self) for _ in range(size_x * size_y // 10)]
        self.__obstacles = obstacles

    def check_limit_planet(self, position):
        if position._Position__x._Coordinate__value > self.__size_x:
            position._Position__x._Coordinate__value = 0
        elif position._Position__x._Coordinate__value < 0:
            position._Position__x._Coordinate__value = self.__size_x
        elif position._Position__y._Coordinate__value > self.__size_y:
            position._Position__y._Coordinate__value = 0
        elif position._Position__y._Coordinate__value < 0:
            position._Position__y._Coordinate__value = self.__size_y
        return position

    def is_obstacle_at_position(self, position) :
        position = self.check_limit_planet(position)
        for obstacle in self.__obstacles :
            if obstacle._Obstacle__position._Position__x._Coordinate__value == position._Position__x._Coordinate__value and obstacle._Obstacle__position._Position__y._Coordinate__value == position._Position__y._Coordinate__value :
                return True
        return False