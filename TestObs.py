import tkinter as tk
import time
import random

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
    def __init__(self, canvas, coord_label):
        self.canvas = canvas
        self.coord_label = coord_label
        self.x = largeur_carte // 2
        self.y = hauteur_carte // 2
        self.direction = "N"
        self.image = canvas.create_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="black")
        self.arrow = None  # Variable pour stocker la flèche
        self.mettre_a_jour_fleche()  # Appeler la méthode pour créer la flèche

    def detecter_collision(self, new_x, new_y):
        for x, y in obstacles:
            if x <= new_x < x + largeur_rover and y <= new_y < y + hauteur_rover:
                obstacle_tag = f"obstacle_{x}_{y}"
                self.canvas.itemconfig(obstacle_tag, fill="red")
                self.coord_label.config(text=f"Obstacle rencontré aux coordonnées : ({x}, {y})")
                return True  # Collision détectée
        return False

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
            if rover.x <= x < rover.x + largeur_rover and rover.y <= y < rover.y + hauteur_rover:
                obstacle_touche = (x, y)

        # Changer la couleur de l'obstacle touché en bleu
        if obstacle_touche is not None:
            obstacle_tag = f"obstacle_{obstacle_touche[0]}_{obstacle_touche[1]}"
            carte.itemconfig(obstacle_tag, fill="red")

        fenetre.update()
        time.sleep(0.3)

        # Revertir la couleur de l'obstacle touché à rouge après l'attente
        if obstacle_touche is not None:
            carte.itemconfig(obstacle_tag, fill="navajowhite")

    # Mettez à jour la fenêtre après avoir traité toutes les commandes
    fenetre.update()

# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Rover sur une carte toroïdale")

# Créer un canevas pour la carte
carte = tk.Canvas(fenetre, width=largeur_carte, height=hauteur_carte, bg="navajowhite")
carte.pack()

# Créer un champ de saisie pour les commandes
champ_commandes = tk.Entry(fenetre)
champ_commandes.pack()

# Créer une étiquette pour afficher les coordonnées de l'obstacle
coord_label = tk.Label(fenetre, text="")
coord_label.pack()

# Créer un rover
rover = Rover(carte, coord_label)

# Créer un bouton pour exécuter les commandes
bouton_executer = tk.Button(fenetre, text="Exécuter", command=executer_commandes)
bouton_executer.pack()

# Quadrillage
for x in range(0, largeur_carte, cell_size):
    carte.create_line(x, 0, x, hauteur_carte, fill="gray")
for y in range(0, hauteur_carte, cell_size):
    carte.create_line(0, y, largeur_carte, y, fill="gray")

# Créez une liste pour stocker les obstacles
obstacles = []

# Fonction pour générer aléatoirement des obstacles dans les cases du quadrillage
def generer_obstacles():
    for _ in range(10):  # Vous pouvez ajuster le nombre d'obstacles à générer
        # Générez une position aléatoire pour les obstacles, en évitant les lignes du quadrillage
        x = random.randrange(0, largeur_carte - largeur_rover, cell_size)
        y = random.randrange(0, hauteur_carte - hauteur_rover, cell_size)

        # Dessinez un carré rouge pour l'obstacle
        obstacle = carte.create_rectangle(x, y, x + largeur_rover, y + hauteur_rover, fill="navajowhite", tags=f"obstacle_{x}_{y}")
        obstacles.append((x, y))

# Appelez la fonction pour générer les obstacles
generer_obstacles()

# Lancer la boucle principale de Tkinter
fenetre.mainloop()
