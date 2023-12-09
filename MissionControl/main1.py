import tkinter as tk
from tkinter import Canvas
import random
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)   
from Domain.MissionRover import rover
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.Topologie.position import Position
from Domain.MissionRover import instruction
from Domain.Exploration.obstacle import Obstacle

def draw_grid(canvas, width, height):
    for x in range(0, width, width // 10):
        canvas.create_line(x, 0, x, height, fill="white")
    for y in range(0, height, height // 10):
        canvas.create_line(0, y, width, y, fill="white")

def draw_obstacles(canvas, obstacles):
    for obstacle in obstacles:
        x = obstacle._Obstacle__position._Position__x._Coordinate__value * (window_width // 10)
        y = obstacle._Obstacle__position._Position__y._Coordinate__value * (window_height // 10)
        canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")

def draw_rover(canvas, rover, color):
    x = rover._Rover__position._Position__x._Coordinate__value * (window_width // 10)
    y = rover._Rover__position._Position__y._Coordinate__value * (window_height // 10)
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color)

def main():
    # Initialiser Tkinter
    root = tk.Tk()
    root.title("Rover UI")

    # Paramètres de la fenêtre
    window_width = 800
    window_height = 600
    grid_size = 20
    rover_color = "green"

    # Initialiser la fenêtre Tkinter
    canvas = Canvas(root, width=window_width, height=window_height, bg="black")
    canvas.pack()

    # Initialiser la planète et le rover
    mars = Planet(10, 10, None)
    curiosity = Rover(0, 0, 'N')
    instructions = instruction.Instruction()

    # Générer aléatoirement des obstacles au début du jeu
    obstacles_list = [Obstacle(mars) for _ in range(random.randint(1, 3))]

    # Dessiner la grille de la planète
    draw_grid(canvas, window_width, window_height)

    # Dessiner les obstacles au début du jeu
    draw_obstacles(canvas, obstacles_list)

    # Dessiner le rover au début du jeu
    draw_rover(canvas, curiosity, rover_color)

    root.update_idletasks()
    root.update()

    # Nettoyer l'écran avant le début du jeu
    time.sleep(2)
    canvas.delete("all")

    while instructions.again:
        # Dessiner la grille de la planète
        draw_grid(canvas, window_width, window_height)

        # Dessiner les obstacles
        draw_obstacles(canvas, obstacles_list)

        # Exécuter les commandes
        instructions.add_instruction()
        curiosity = instructions.exec_commands(mars, curiosity)
        is_obstacle = False

        # Dessiner le rover à sa nouvelle position
        draw_rover(canvas, curiosity, rover_color)

        # Mettre à jour l'écran
        root.update_idletasks()
        root.update()

        # Attendre un court instant
        time.sleep(0.5)

    # Quitter Tkinter
    root.destroy()

if __name__ == "__main__":
    main()
