from Domain.MissionRover import rover
from Domain.Exploration import planet
from Domain.MissionRover import instruction
from Domain.Topologie import position
from Domain.Exploration import obstacle


def main():
    mars = planet.Planet(5, 5, None)
    #print(obstacle._Obstacle__position._Position__x._Coordinate__value)
    curiosity = rover.Rover(0, 0, 'N')
    instructions = instruction.Instruction()

    while instructions.again:
        instructions.add_instruction()
        curiosity = instructions.exec_commands(mars, curiosity)

if __name__ == '__main__':
    main()
