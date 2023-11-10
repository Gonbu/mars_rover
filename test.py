import tkinter as tk
import time
import random
from math import cos, sin, radians

# Dimensions de la carte toroïdale
largeur_carte = 500
hauteur_carte = 500

# Dimensions du rover
largeur_rover = 20
hauteur_rover = 20

# Calcul de la taille des cellules de la grille en fonction des dimensions du rover
cell_size = max(largeur_rover, hauteur_rover)

# Classe pour représenter le rover
class Rover:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = largeur_carte // 2
        self.y = hauteur_carte // 2
        self.direction = "N"
        self.image = canvas.create_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="black")
        self.arrow = None  # Variable pour stocker la flèche
        self.mettre_a_jour_fleche()  # Appeler la méthode pour créer la flèche

    def mettre_a_jour_fleche(self):
        if self.arrow:
            self.canvas.delete(self.arrow)
        x1, y1, x2, y2, x3, y3 = self.calculer_points_fleche()
        self.arrow = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="Grey")

    def avancer(self):
        new_x, new_y = self.x, self.y
        if self.direction == "N":
            new_y = (self.y - cell_size) % hauteur_carte
        elif self.direction == "S":
            new_y = (self.y + cell_size) % hauteur_carte
        elif self.direction == "E":
            new_x = (self.x + cell_size) % largeur_carte
        elif self.direction == "W":
            new_x = (self.x - cell_size) % largeur_carte

        if not self.detecter_collision(new_x, new_y):
            self.x, self.y = new_x, new_y
            self.canvas.coords(self.image, self.x - 10, self.y - 10, self.x + 10, self.y + 10)
            self.mettre_a_jour_fleche()

    def reculer(self):
        new_x, new_y = self.x, self.y
        if self.direction == "N":
            new_y = (self.y + cell_size) % hauteur_carte
        elif self.direction == "S":
            new_y = (self.y - cell_size) % hauteur_carte
        elif self.direction == "E":
            new_x = (self.x - cell_size) % largeur_carte
        elif self.direction == "W":
            new_x = (self.x + cell_size) % largeur_carte

        if not self.detecter_collision(new_x, new_y):
            self.x, self.y = new_x, new_y
            self.canvas.coords(self.image, self.x - 10, self.y - 10, self.x + 10, self.y + 10)
            self.mettre_a_jour_fleche()

             # Ajouter une méthode pour détecter la collision
    def detecter_collision(self, new_x, new_y):
        for x, y in obstacles:
            if x <= new_x < x + largeur_rover and y <= new_y < y + hauteur_rover:
                obstacle_tag = f"obstacle_{x}_{y}"
                self.canvas.itemconfig(obstacle_tag, fill="red")
                return True  # Collision détectée
        return False

    def tourner_droite(self):
        directions = ["N", "E", "S", "W"]
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]
        self.mettre_a_jour_fleche()

    def tourner_gauche(self):
        directions = ["N", "W", "S", "E"]
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]
        self.mettre_a_jour_fleche()

    def calculer_points_fleche(self):
        angle = radians(30)  # Angle pour définir la direction de la flèche
        length = 15  # Longueur de la flèche
        x, y = self.x, self.y

        if self.direction == "N":
            return x, y - length, x - length * sin(angle), y + length * cos(angle), x + length * sin(angle), y + length * cos(angle)
        elif self.direction == "S":
            return x, y + length, x - length * sin(angle), y - length * cos(angle), x + length * sin(angle), y - length * cos(angle)
        elif self.direction == "E":
            return x + length, y, x - length * cos(angle), y - length * sin(angle), x - length * cos(angle), y + length * sin(angle)
        elif self.direction == "W":
            return x - length, y, x + length * cos(angle), y - length * sin(angle), x + length * cos(angle), y + length * sin(angle)

# Fonction pour exécuter les commandes une par une
def executer_commandes():
    commandes = champ_commandes.get()
    for commande in commandes:
        obstacle_touche = None  # Variable pour stocker l'obstacle touché

        if commande == "F":
            rover.avancer()
        elif commande == "B":
            rover.reculer()
        elif commande == "R":
            rover.tourner_droite()
        elif commande == "L":
            rover.tourner_gauche()

        # Vérifier s'il y a une collision avec un obstacle
        for x, y in obstacles:
            if x <= rover.x < x + largeur_rover and y <= rover.y < y + hauteur_rover:
                obstacle_touche = (x, y)

        # Changer la couleur de l'obstacle touché en bleu
        if obstacle_touche is not None:
            obstacle_tag = f"obstacle_{obstacle_touche[0]}_{obstacle_touche[1]}"
            carte.itemconfig(obstacle_tag, fill="red")

        fenetre.update()
        time.sleep(0.3)

        # Revertir la couleur de l'obstacle touché à rouge après l'attente
        #if obstacle_touche is not None:
        #    obstacle_tag = f"obstacle_{obstacle_touche[0]}_{obstacle_touche[1]}"
        #    carte.itemconfig(obstacle_tag, fill="red")

    # Mettez à jour la fenêtre après avoir traité toutes les commandes
    fenetre.update()



# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Rover sur une carte toroïdale")

# Créer un canevas pour la carte
carte = tk.Canvas(fenetre, width=largeur_carte, height=hauteur_carte, bg="navajowhite")
carte.pack()

# Créer un rover
rover = Rover(carte)

# Créer un champ de saisie pour les commandes
champ_commandes = tk.Entry(fenetre)
champ_commandes.pack()

# Créer un bouton pour exécuter les commandes
bouton_executer = tk.Button(fenetre, text="Exécuter", command=executer_commandes)
bouton_executer.pack()

# Quadrillage
for x in range(0, largeur_carte, cell_size):
    carte.create_line(x, 0, x, hauteur_carte, fill="gray")
for y in range(0, hauteur_carte, cell_size):
    carte.create_line(0, y, largeur_carte, y, fill="gray")

# Créez une liste pour stocker les obstacles
obstacles = {}

# Fonction pour générer aléatoirement des obstacles dans les cases du quadrillage
def generer_obstacles():
    for _ in range(10):
        x = random.randrange(0, largeur_carte - largeur_rover, cell_size)
        y = random.randrange(0, hauteur_carte - hauteur_rover, cell_size)
        obstacle_tag = f"obstacle_{x}_{y}"
        obstacle = carte.create_rectangle(x, y, x + largeur_rover, y + hauteur_rover, fill="navajowhite", tags=obstacle_tag)
        obstacles[(x, y)] = obstacle_tag
# Appelez la fonction pour générer les obstacles
generer_obstacles()

# Lancer la boucle principale de Tkinter
fenetre.mainloop()
