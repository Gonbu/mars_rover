import sys
import os

from roverFront import RoverFront
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Domain.MissionRover.command import Command

import tkinter as tk

largeur_carte = 500
hauteur_carte = 500

# Dimensions du rover
largeur_rover = 20
hauteur_rover = 20

# Calcul de la taille des cellules de la grille en fonction des dimensions du rover
cell_size = max(largeur_rover, hauteur_rover)
class MissionControlRunner:
    def __init__(self, sender, receiver, protocol, rover, server_address):
        self.sender = sender
        self.receiver = receiver
        self.protocol = protocol
        self.rover = rover
        self.server_address = server_address
        self.fenetre = None

    def run(self):
        try:
            while True:
                commands = Command()
                commands.add_command()

                self.sender.send_command(self.protocol, commands._Command__command_order)
                self.rover, obstacle = self.receiver.receive_command(self.protocol, self.rover)

                self.rover.to_string()
                if len(obstacle) > 0:
                    print("Obstacle : {}".format(obstacle))
        finally:
            self.protocol.client_socket.close()

    def execute_commands(self, commandlist=None):
        commandlist = list(commandlist.replace(" ", ""))
        print(commandlist)
        if not commandlist :
            commands = Command()
            commands.add_command()
        else :
            commands = Command(commandlist)

        self.sender.send_command(self.protocol, commands._Command__command_order)
        self.rover, obstacle = self.receiver.receive_command(self.protocol, self.rover)

        self.rover.to_string()
        if len(obstacle) > 0:
            print("Obstacle : {}".format(obstacle))

    def init_front(self) :
                
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
        rover = RoverFront(carte, coord_label)

        # Créer un bouton pour exécuter les commandes
        bouton_executer = tk.Button(fenetre, text="Exécuter", command=lambda: self.execute_commands(champ_commandes.get()))
        bouton_executer.pack()

        # Quadrillage
        for x in range(0, largeur_carte, cell_size):
            carte.create_line(x, 0, x, hauteur_carte, fill="gray")
        for y in range(0, hauteur_carte, cell_size):
            carte.create_line(0, y, largeur_carte, y, fill="gray")

        # Lancer la boucle principale de Tkinter
        fenetre.mainloop()
