# CommunicationAbstraction.py

from abc import ABC, abstractmethod

class CommandSender(ABC):
    @abstractmethod
    def send_command(self, command):
        pass

class CommandReceiver(ABC):
    @abstractmethod
    def receive_command(self):
        pass
