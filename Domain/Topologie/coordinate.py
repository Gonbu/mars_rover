#Objet-valeur
class Coordinate:
    def __init__(self, value):
        self.__value = value

    def modulo(self, size_planet) :
        return self.__value % (size_planet + 1)
    
    def compare(self, other_coordinate):
        return self.__value == other_coordinate._Coordinate__value
    
    def __eq__(self, other_coordinate) :
        return self.__value == other_coordinate._Coordinate__value