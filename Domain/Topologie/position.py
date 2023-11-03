from Domain.Topologie.coordinate import Coordinate

#Objet-valeur
class Position:
    def __init__(self, x, y) -> None:
        self.__x = Coordinate(x)
        self.__y = Coordinate(y)
