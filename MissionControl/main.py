import socket
import pickle
import threading
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from MissionControl.missionControlRunner import MissionControlRunner
from Domain.MissionRover.rover import Rover
from Domain.Exploration.planet import Planet
from Domain.MissionRover.command import Command
from Domain.Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
from SocketCommunication.ReceiverFromRover import ReceiverFromRover
from SocketCommunication.SenderToRover import SenderToRover
from Missions.marsMission import *


def main() :
    sender = SenderToRover()
    receiver = ReceiverFromRover()
    protocol = MyCommunicationProtocol(sender, receiver)
    protocol.establish_connection(mission_control_connection_address)

    rover = Rover(position_x_start, position_y_start, orientation_start)

    mission_control_runner = MissionControlRunner(sender, receiver, protocol, rover, mission_control_connection_address)
    mission_control_runner.init_front()
    #mission_control_runner.run()

if __name__ == "__main__":
    main()
