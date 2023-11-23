import socket
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Rover.roverOverNetwork import RoverOverNetwork
from Domain.MissionRover.rover import Rover
from Domain.MissionRover.command import Command
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
from SocketCommunication.ReceiverFromMissionControl import ReceiverFromMissionControl
from SocketCommunication.SenderToMissionControl import SenderToMissionControl
from Missions.marsMission import *

def main():
    sender = SenderToMissionControl()
    receiver = ReceiverFromMissionControl()
    protocol = MyCommunicationProtocol(sender, receiver)

    protocol.initialize_server(rover_address)

    rover_at_start = Rover(position_x_start, position_y_start, orientation_start)
    rover_over_network = RoverOverNetwork(rover_at_start, protocol, sender, receiver, mars)

    rover_over_network.run()

if __name__ == "__main__":
    main()
