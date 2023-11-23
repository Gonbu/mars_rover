from Domain.Exploration.planet import Planet

mars = Planet(size_x=5, size_y=5)
position_x_start = 0
position_y_start = 0
orientation_start = 'N'
rover_address = ('127.0.0.1', 12345)
repeater_address = ('127.0.0.1', 12346)
mission_control_connection_address = rover_address
