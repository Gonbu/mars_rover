from Domain.Exploration.planet import Planet


size_x_planet=5
size_y_planet=5
mars = Planet(size_x=size_x_planet, size_y=size_y_planet)
position_x_start = 0
position_y_start = 0
orientation_start = 'N'
rover_address = ('127.0.0.1', 12345)
repeater_address = ('127.0.0.1', 12346)
mission_control_connection_address = rover_address

# Dimensions de la carte toroïdale
largeur_carte = 500
hauteur_carte = 500

# Dimensions du rover
largeur_rover = largeur_carte // (size_x_planet + 1)
hauteur_rover = hauteur_carte // (size_y_planet + 1)

# Calcul de la taille des cellules de la grille en fonction des dimensions du rover
cell_size = max(largeur_rover, hauteur_rover)
