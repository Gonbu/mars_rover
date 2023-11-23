import socket
import pickle
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from Repeater.repeaterRunner import RepeaterRunner
from Domain.MissionRover.rover import Rover
from Domain.MissionRover.command import Command
from Domain.Communication.CommunicationAbstraction import CommandSender, CommandReceiver
from SocketCommunication.ProtocolCommunication import MyCommunicationProtocol
from SocketCommunication.ReceiverFromRover import ReceiverFromRover
from SocketCommunication.SenderToRover import SenderToRover
from SocketCommunication.ReceiverFromMissionControl import ReceiverFromMissionControl
from SocketCommunication.SenderToMissionControl import SenderToMissionControl
from Missions.marsMission import *

def main() :
    sender_mission_control = SenderToMissionControl()
    receiver_mission_control = ReceiverFromMissionControl()

    sender_rover = SenderToRover()
    receiver_rover = ReceiverFromRover()

    protocol_server = MyCommunicationProtocol(sender_mission_control, receiver_mission_control)
    protocol_client = MyCommunicationProtocol(sender_rover, receiver_rover)
        
    protocol_server.initialize_server(repeater_address)
    protocol_client.establish_connection(rover_address)
    
    rover = Rover(position_x_start, position_y_start, orientation_start)

    repeater_runner = RepeaterRunner(sender_mission_control, receiver_mission_control, sender_rover, receiver_rover, protocol_server, protocol_client, rover)
    repeater_runner.run()

if __name__ == "__main__":
    main()
