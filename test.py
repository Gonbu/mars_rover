import tkinter as tk
import time

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
        self.image = canvas.create_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill="blue")

    def avancer(self):
        if self.direction == "N":
            self.y = (self.y - cell_size) % hauteur_carte
        elif self.direction == "S":
            self.y = (self.y + cell_size) % hauteur_carte
        elif self.direction == "E":
            self.x = (self.x + cell_size) % largeur_carte
        elif self.direction == "W":
            self.x = (self.x - cell_size) % largeur_carte
        self.canvas.coords(self.image, self.x - 10, self.y - 10, self.x + 10, self.y + 10)

    def reculer(self):
        if self.direction == "N":
            self.y = (self.y + cell_size) % hauteur_carte
        elif self.direction == "S":
            self.y = (self.y - cell_size) % hauteur_carte
        elif self.direction == "E":
            self.x = (self.x - cell_size) % largeur_carte
        elif self.direction == "W":
            self.x = (self.x + cell_size) % largeur_carte
        self.canvas.coords(self.image, self.x - 10, self.y - 10, self.x + 10, self.y + 10)

    def tourner_droite(self):
        directions = ["N", "E", "S", "W"]
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]

    def tourner_gauche(self):
        directions = ["N", "W", "S", "E"]
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]

# Fonction pour exécuter les commandes une par une
def executer_commandes():
    commandes = champ_commandes.get()
    for commande in commandes:
        if commande == "F":
            rover.avancer()
        elif commande == "B":
            rover.reculer()
        elif commande == "R":
            rover.tourner_droite()
        elif commande == "L":
            rover.tourner_gauche()
        fenetre.update()  # Mettre à jour la fenêtre pour afficher le mouvement du rover
        time.sleep(0.3)  # Pause d'une seconde entre chaque commande

# Créer une fenêtre Tkinter
fenetre = tk.Tk()
fenetre.title("Rover sur une carte toroïdale")

# Créer un canevas pour la carte
carte = tk.Canvas(fenetre, width=largeur_carte, height=hauteur_carte, bg="white")
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


# Lancer la boucle principale de Tkinter
fenetre.mainloop()
