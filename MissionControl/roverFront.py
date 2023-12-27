import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Missions.marsMission import *
from Domain.MissionRover.rover import Rover

# Classe pour représenter le rover
class RoverFront(Rover):
    def __init__(self, canvas, coord_label):
        self.canvas = canvas
        self.coord_label = coord_label
        self.x = position_x_start * largeur_rover + largeur_rover // 2
        self.y = largeur_carte - (largeur_carte%largeur_rover) - position_y_start * hauteur_rover - hauteur_rover // 2
        self.direction = "N"
        self.image = canvas.create_rectangle(self.x - largeur_rover // 2, self.y - hauteur_rover // 2, self.x + largeur_rover // 2, self.y + hauteur_rover // 2, fill="black")
        self.arrow = None  # Variable pour stocker la flèche
        self.mettre_a_jour_fleche()  # Appeler la méthode pour créer la flèche

    def updatePosition(self, rover):
        new_coords = str(rover._Rover__position).split(",")
        self.x = int(new_coords[0]) * largeur_rover + largeur_rover // 2
        self.y = largeur_carte - (largeur_carte%largeur_rover) - int(new_coords[1]) * hauteur_rover - hauteur_rover // 2
        self.canvas.coords(self.image, self.x - largeur_rover // 2, self.y - hauteur_rover // 2, self.x + largeur_rover // 2, self.y + hauteur_rover // 2)
        self.direction = (str(rover._Rover__orientation))
        self.mettre_a_jour_fleche()

    def mettre_a_jour_fleche(self):
        if self.arrow:
            self.canvas.delete(self.arrow)
        x1, y1, x2, y2, x3, y3 = self.calculer_points_fleche()
        self.arrow = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="grey")

    def calculer_points_fleche(self):
        angle = 30  # Angle pour définir la direction de la flèche
        length = 15  # Longueur de la flèche
        x, y = self.x, self.y

        if self.direction == "N":
            return x, y - length, x - length * 0.5, y + length * 0.87, x + length * 0.5, y + length * 0.87
        elif self.direction == "S":
            return x, y + length, x - length * 0.5, y - length * 0.87, x + length * 0.5, y - length * 0.87
        elif self.direction == "E":
            return x + length, y, x - length * 0.87, y - length * 0.5, x - length * 0.87, y + length * 0.5
        elif self.direction == "W":
            return x - length, y, x + length * 0.87, y - length * 0.5, x + length * 0.87, y + length * 0.5
