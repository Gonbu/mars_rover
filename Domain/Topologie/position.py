from Domain.Topologie.coordinate import Coordinate

#Objet-valeur
class Position:
    def __init__(self, x, y) -> None:
        self.__x = Coordinate(x)
        self.__y = Coordinate(y)

    def modulo(self, size_planet_x, size_planet_y) :
        return self.__x.modulo(size_planet_x), self.__y.modulo(size_planet_y)
        
    def __eq__(self, other_position) :
        return self.__x == other_position._Position__x and self.__y == other_position._Position__y

    def __str__(self) :
        return f"{self.__x},{self.__y}"

    
