from Domain.Topologie.position import Position
from random import randint

#Objet-valeur
class Obstacle:
    def __init__(self, planet, position = None):
        if position is None :
            position = Position(
                randint(0, planet._Planet__size_x),
                randint(0, planet._Planet__size_y),
            )
        self.__position = position
    
    def compare_obstacle_and_position(self, compared_position) :
        return self.__position == compared_position