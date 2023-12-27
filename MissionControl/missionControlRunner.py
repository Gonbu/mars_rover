import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from MissionControl.roverFront import RoverFront
from Domain.MissionRover.command import Command

from Missions.marsMission import *
import tkinter as tk

class MissionControlRunner:
    def __init__(self, sender, receiver, protocol, rover, server_address):
        self.sender = sender
        self.receiver = receiver
        self.protocol = protocol
        self.rover = rover
        self.server_address = server_address
        self.carte = None

    def execute_commands(self, commandlist=None, rover_front=None):
        commandlist = list(commandlist.replace(" ", ""))
        print(commandlist)
        if not commandlist :
            commands = Command()
            commands.add_command()
        else :
            commands = Command(commandlist)

        self.sender.send_command(self.protocol, commands._Command__command_order)
        self.rover, obstacle = self.receiver.receive_command(self.protocol, self.rover)

        self.rover.display_state()
        if len(obstacle) > 0:
            print("Obstacle : {}".format(obstacle))
            x, y = obstacle
            x = x * largeur_rover + largeur_rover // 2
            y = largeur_carte - (largeur_carte%largeur_rover) - y * hauteur_rover - hauteur_rover // 2
            self.carte.create_rectangle(x - largeur_rover // 2, y - hauteur_rover // 2, x + largeur_rover // 2, y + hauteur_rover // 2, fill="red")

        if rover_front :
            rover_front.updatePosition(self.rover)

    def init_front(self) :
                
        # Créer une fenêtre Tkinter
        fenetre = tk.Tk()
        fenetre.title("Rover sur une carte toroïdale")

        # Créer un canevas pour la carte
        self.carte = tk.Canvas(fenetre, width=largeur_carte, height=hauteur_carte, bg="navajowhite")
        self.carte.pack()

        # Créer un champ de saisie pour les commandes
        champ_commandes = tk.Entry(fenetre)
        champ_commandes.pack()

        # Créer une étiquette pour afficher les coordonnées de l'obstacle
        coord_label = tk.Label(fenetre, text="")
        coord_label.pack()

        # Créer un rover
        rover_front = RoverFront(self.carte, coord_label)

        # Créer un bouton pour exécuter les commandes
        bouton_executer = tk.Button(fenetre, text="Exécuter", command=lambda: self.execute_commands(champ_commandes.get(), rover_front))
        bouton_executer.pack()

        # Quadrillage
        for x in range(0, largeur_carte, cell_size):
            self.carte.create_line(x, 0, x, hauteur_carte, fill="gray")
        for y in range(0, hauteur_carte, cell_size):
            self.carte.create_line(0, y, largeur_carte, y, fill="gray")

        # Lancer la boucle principale de Tkinter
        fenetre.mainloop()
