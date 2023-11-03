from abc import ABC, abstractmethod

class PlanetInterface(ABC):
    @abstractmethod
    def __init__(self, size_x, size_y, obstacles=None):
        pass
    
    @abstractmethod
    def check_limit_planet(self, position):
        pass

    @abstractmethod
    def is_obstacle_at_position(self, position) :
        pass