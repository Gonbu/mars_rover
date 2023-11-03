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
    