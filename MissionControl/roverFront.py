# Dimensions de la carte toroïdale
largeur_carte = 500
hauteur_carte = 500

# Dimensions du rover
largeur_rover = 20
hauteur_rover = 20

# Calcul de la taille des cellules de la grille en fonction des dimensions du rover
cell_size = max(largeur_rover, hauteur_rover)

# Classe pour représenter le rover
class RoverFront:
    def __init__(self, canvas, coord_label):
        self.canvas = canvas
        self.coord_label = coord_label
        self.x = largeur_carte // 2
        self.y = hauteur_carte // 2
        self.direction = "N"
        self.image = canvas.create_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="black")
        self.arrow = None  # Variable pour stocker la flèche
        self.mettre_a_jour_fleche()  # Appeler la méthode pour créer la flèche

    def updatePosition(self, new_x, new_y):
        self.x, self.y = new_x, new_y
        self.canvas.coords(self.image, self.x - 10, self.y - 10, self.x + 10, self.y + 10)
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
