import pygame
from pygame.locals import QUIT
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)   
from Domain.MissionRover import rover
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.Topologie.position import Position
from Domain.MissionRover import instruction
from Domain.Exploration.obstacle import Obstacle

def main():
    # Initialiser Pygame
    pygame.init()

    # Paramètres de la fenêtre
    window_width = 800
    window_height = 600
    grid_size = 20
    rover_color = (0, 255, 0)

    # Initialiser la fenêtre Pygame
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Rover UI")

    # Initialiser la planète et le rover
    mars = Planet(10, 10, None)
    curiosity = Rover(0, 0, 'N')
    instructions = instruction.Instruction()
    
    # Dessiner la grille de la planète
    for x in range(0, window_width, window_width // 10):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, window_height))
    for y in range(0, window_height, window_height // 10):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (window_width, y))
    
    # Générer aléatoirement des obstacles au début du jeu
    obstacles_list = [Obstacle(mars) for _ in range(random.randint(1, 3))]

    # Dessiner les obstacles uniquement au début du jeu
    for obstacle in obstacles_list:
        obstacle_x = obstacle._Obstacle__position._Position__x._Coordinate__value * (window_width // 10)
        obstacle_y = obstacle._Obstacle__position._Position__y._Coordinate__value * (window_height // 10)
        pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, 20, 20))
    
    # Dessiner le rover une seule fois au début du jeu
    rover_x = curiosity._Rover__position._Position__x._Coordinate__value * (window_width // 10)
    rover_y = curiosity._Rover__position._Position__y._Coordinate__value * (window_height // 10)
    pygame.draw.circle(screen, rover_color, (rover_x, rover_y), 10)
    
    # Nettoyer l'écran avant le début du jeu
    #screen.fill((0, 0, 0))
    # Déclarer les variables pour la dernière position du rover
    rover_x_last, rover_y_last = rover_x, rover_y
    
    while instructions.again:
        pygame.event.pump()
           
        # Dessiner la grille de la planète
        for x in range(0, window_width, window_width // 10):
            pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, window_height))
        for y in range(0, window_height, window_height // 10):
            pygame.draw.line(screen, (255, 255, 255), (0, y), (window_width, y))

        # Dessiner les obstacles
        for obstacle in obstacles_list:
            obstacle_x = obstacle._Obstacle__position._Position__x._Coordinate__value * (window_width // 10)
            obstacle_y = obstacle._Obstacle__position._Position__y._Coordinate__value * (window_height // 10)
            pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, 20, 20))

        #instructions.add_instruction()
        #curiosity = instructions.exec_commands(mars, curiosity)
        
        # Exécuter les commandes
        instructions.add_instruction()
        curiosity = instructions.exec_commands(mars, curiosity)
        is_obstacle = False
        
        # Dessiner le rover à sa nouvelle position
        rover_x = curiosity._Rover__position._Position__x._Coordinate__value * (window_width // 10)
        rover_y = curiosity._Rover__position._Position__y._Coordinate__value * (window_height // 10)

        if is_obstacle:
            # Laisser un carré rouge pour représenter un obstacle
            pygame.draw.rect(screen, (255, 0, 0), (rover_x, rover_y, 20, 20))
        else:
            # Mise à jour de la position du rover dans la grille sans laisser de trace
            pygame.draw.circle(screen, (0, 0, 0), (int(rover_x_last), int(rover_y_last)), 10)
            pygame.draw.circle(screen, rover_color, (rover_x, rover_y), 10)
        
        # Mettre à jour la dernière position du rover
        rover_x_last, rover_y_last = rover_x, rover_y

        # Mettre à jour l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()

if __name__ == "__main__":
    main()